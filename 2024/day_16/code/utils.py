# Third-party imports
import branca
import folium
import geopandas as gpd
import pandas as pd
import requests
from rtree import index
from shapely.geometry import Point, shape
from shapely.prepared import prep


def get_sf_trees() -> pd.DataFrame:
    """
    Fetch tree data from San Francisco's open data API.
    """
    api_endpoint = "https://data.sfgov.org/resource/tkzw-k3nq.json"
    api_params = {"$limit": 2000000, "$offset": 0}
    api_response = requests.get(api_endpoint, params=api_params)
    api_response.raise_for_status()
    trees_df = pd.DataFrame(api_response.json())
    trees_df = trees_df.astype({"latitude": "float64", "longitude": "float64"})
    return trees_df


def get_zipcode(lat: float, lon: float, sf_zips: dict) -> tuple[str, shape] | None:
    """
    Find the zipcode and polygon for given coordinates within San Francisco.
    """
    point = Point(lon, lat)
    for feature in sf_zips["features"]:
        polygon = shape(feature["geometry"])
        if polygon.contains(point):
            return feature["properties"]["zip"], polygon
    return None


def add_zipcodes_to_df(trees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add zipcode and geometry information to the trees DataFrame using spatial indexing.
    """
    trees_df["latitude"] = pd.to_numeric(trees_df["latitude"], errors="coerce")
    trees_df["longitude"] = pd.to_numeric(trees_df["longitude"], errors="coerce")

    geojson_url = "https://data.sfgov.org/api/geospatial/uq3t-6t53?method=export&format=GeoJSON"
    zipcode_boundaries = requests.get(geojson_url).json()

    spatial_index = index.Index()
    zipcode_polygons = {}
    
    for feature_idx, feature in enumerate(zipcode_boundaries["features"]):
        try:
            current_polygon = shape(feature["geometry"])
            polygon_bounds = list(current_polygon.bounds)

            min_x, max_x = min(polygon_bounds[0], polygon_bounds[2]), max(polygon_bounds[0], polygon_bounds[2])
            min_y, max_y = min(polygon_bounds[1], polygon_bounds[3]), max(polygon_bounds[1], polygon_bounds[3])

            if min_x == max_x:
                max_x += 0.0000001
            if min_y == max_y:
                max_y += 0.0000001

            spatial_index.insert(feature_idx, (min_x, min_y, max_x, max_y))
            zipcode_polygons[feature_idx] = (current_polygon, feature["properties"]["zip"])

        except Exception as error:
            print(f"Skipping feature {feature_idx} due to error: {error}")
            print(f"Bounds were: {current_polygon.bounds}")
            continue

    prepared_zipcode_polygons = {
        idx: (prep(poly), zipcode) for idx, (poly, zipcode) in zipcode_polygons.items()
    }

    tree_points = [
        Point(longitude, latitude) 
        for longitude, latitude in zip(trees_df["longitude"], trees_df["latitude"])
    ]

    zipcode_assignments = []
    for tree_point in tree_points:
        match_found = False
        try:
            point_bbox = (tree_point.x, tree_point.y, tree_point.x, tree_point.y)
            for polygon_idx in spatial_index.intersection(point_bbox):
                prepared_polygon, zipcode = prepared_zipcode_polygons[polygon_idx]
                if prepared_polygon.contains(tree_point):
                    zipcode_assignments.append((zipcode, zipcode_polygons[polygon_idx][0]))
                    match_found = True
                    break
            if not match_found:
                zipcode_assignments.append((None, None))
        except Exception as error:
            print(f"Error processing point {tree_point}: {error}")
            zipcode_assignments.append((None, None))

    zipcodes, geometries = zip(*zipcode_assignments)
    trees_df["zipcode"] = zipcodes
    trees_df["zipcode_geom"] = geometries

    return trees_df


def create_choropleth_map(agg_trees_gdf: gpd.GeoDataFrame) -> folium.Map:
    """
    Create a choropleth map visualization of trees by zipcode.
    """
    sf_map = folium.Map(
        location=[37.7749, -122.4194], zoom_start=12, tiles="cartodbpositron"
    )

    colormap = branca.colormap.LinearColormap(
        colors=["#ffffff", "#90c890"],
        vmin=agg_trees_gdf["count"].min(),
        vmax=agg_trees_gdf["count"].max(),
        caption="Number of Trees",
    )

    folium.GeoJson(
        agg_trees_gdf,
        style_function=lambda x: {
            "fillColor": f'#{
                int(255 - 111 * (x["properties"]["count"] - agg_trees_gdf["count"].min()) / 
                    (agg_trees_gdf["count"].max() - agg_trees_gdf["count"].min())):02x}{
                int(255 - 55 * (x["properties"]["count"] - agg_trees_gdf["count"].min()) /
                    (agg_trees_gdf["count"].max() - agg_trees_gdf["count"].min())):02x}{
                int(255 - 111 * (x["properties"]["count"] - agg_trees_gdf["count"].min()) /
                    (agg_trees_gdf["count"].max() - agg_trees_gdf["count"].min())):02x}',
            "fillOpacity": 0.9,
            "color": "black",
            "weight": 1,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["zipcode", "count"],
            aliases=["ZIP Code:", "Number of Trees:"],
            style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;",
        ),
        popup=folium.GeoJsonPopup(
            fields=["zipcode", "count"],
            aliases=["ZIP Code:", "Number of Trees:"],
            style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;",
        ),
    ).add_to(sf_map)

    colormap.add_to(sf_map)
    title_html = """
        <h3 align="center" style="font-size:16px">
            <b>San Francisco Street Trees by ZIP Code</b>
        </h3>
    """
    sf_map.get_root().html.add_child(folium.Element(title_html))
    return sf_map
