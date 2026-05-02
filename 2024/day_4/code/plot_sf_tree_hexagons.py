import pandas as pd
import geopandas as gpd
import h3
import matplotlib.pyplot as plt
import requests
from shapely.geometry import Polygon
import os

def get_sf_trees():
    """Fetch tree data from San Francisco's open data API."""
    api_endpoint = "https://data.sfgov.org/resource/tkzw-k3nq.json"
    # Limit to 50k for performance in this exercise
    api_params = {"$limit": 50000, "$offset": 0}
    response = requests.get(api_endpoint, params=api_params)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df = df.astype({"latitude": "float64", "longitude": "float64"})
    return df.dropna(subset=['latitude', 'longitude'])

def main():
    print("Fetching tree data...")
    df = get_sf_trees()
    
    print("Binning into H3 hexagons...")
    resolution = 9
    df['h3_cell'] = df.apply(lambda row: h3.latlng_to_cell(row['latitude'], row['longitude'], resolution), axis=1)
    
    # Count trees per cell
    counts = df['h3_cell'].value_counts().reset_index()
    counts.columns = ['h3_cell', 'tree_count']
    
    # Convert H3 cells to polygons
    print("Converting cells to polygons...")
    def cell_to_polygon(cell):
        boundary = h3.cell_to_boundary(cell)
        # H3 returns (lat, lng), shapely expects (lng, lat)
        return Polygon([(lng, lat) for lat, lng in boundary])
    
    counts['geometry'] = counts['h3_cell'].apply(cell_to_polygon)
    gdf = gpd.GeoDataFrame(counts, geometry='geometry', crs="EPSG:4326")
    
    # Project to UTM Zone 10N for better visualization
    gdf = gdf.to_crs(epsg=26910)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0b0d0f')
    ax.set_facecolor('#0b0d0f')
    
    gdf.plot(
        ax=ax, 
        column='tree_count', 
        cmap='Greens', 
        edgecolor='none',
        legend=True,
        legend_kwds={'label': "Tree Count per Hexagon", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    ax.set_axis_off()
    ax.set_title('San Francisco Street Tree Density', color='white', fontsize=20, pad=20, fontweight='bold')
    
    output_path = os.path.join('2024', 'day_4', 'visualization', 'sf_tree_hexagons.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0b0d0f')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
