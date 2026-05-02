import osmnx as ox
import pydeck as pdk
import pandas as pd
import os

def main():
    print("Fetching SF building data...")
    # Center on Financial District / Market St
    center = (37.791, -122.398)
    
    # Get building footprints with heights
    # We use features_from_point to get a small manageable area
    tags = {'building': True}
    gdf = ox.features_from_point(center, tags=tags, dist=500)
    
    # Clean up and ensure height exists
    # Height is often a string in OSM, need to parse
    def parse_height(h):
        if pd.isna(h): return 10 # Default height
        try:
            # Handle cases like '10 m' or '15.5'
            return float(str(h).split()[0])
        except:
            return 10

    print("Processing building heights...")
    if 'height' in gdf.columns:
        gdf['height_num'] = gdf['height'].apply(parse_height)
    else:
        gdf['height_num'] = 15 # Default
    
    # Prepare for pydeck (needs to be in a standard CRS or just lat/lon)
    gdf = gdf.to_crs(epsg=4326)
    
    # Pydeck works better with flat dataframes for simple layers
    # Extract coordinates for polygons
    def get_coords(geom):
        if geom.geom_type == 'Polygon':
            return list(geom.exterior.coords)
        elif geom.geom_type == 'MultiPolygon':
            # Just take the first one for simplicity in this visualization
            return list(geom.geoms[0].exterior.coords)
        return None

    gdf['polygon_coords'] = gdf.geometry.apply(get_coords)
    gdf = gdf.dropna(subset=['polygon_coords'])
    
    print("Creating 3D map with pydeck...")
    # Define a layer
    layer = pdk.Layer(
        "PolygonLayer",
        gdf,
        id="buildings",
        get_polygon="polygon_coords",
        get_elevation="height_num",
        get_fill_color="[200, 30, 0, 160]",
        pickable=True,
        extruded=True,
    )
    
    # Set the view
    view_state = pdk.ViewState(
        latitude=center[0],
        longitude=center[1],
        zoom=15,
        pitch=45,
        bearing=0
    )
    
    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/dark-v10")
    
    output_path = os.path.join('2024', 'day_18', 'visualization', 'sf_3d_buildings.html')
    r.to_html(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
