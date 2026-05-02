import osmnx as ox
import matplotlib.pyplot as plt
import os
import geopandas as gpd
from shapely.geometry import LineString

def main():
    print("Generating 'Desire Lines' collaborative map...")
    location = "San Francisco, California, USA"
    
    # 1. Fetch 'Official' infrastructure (Bike paths)
    print("Fetching official bike infrastructure...")
    official_gdf = ox.features_from_place(location, tags={'highway': 'cycleway'})
    
    # 2. Simulate 'User' paths (Desire lines)
    # We'll create some synthetic 'popular' routes that might not be on official paths
    print("Simulating user-generated 'desire lines'...")
    desire_lines = [
        LineString([(-122.41, 37.76), (-122.43, 37.77)]), # Mission to Lower Haight
        LineString([(-122.45, 37.76), (-122.47, 37.78)]), # Golden Gate Park diagonal
        LineString([(-122.40, 37.78), (-122.42, 37.80)]), # Market to Pier
    ]
    user_gdf = gpd.GeoDataFrame(geometry=desire_lines, crs="EPSG:4326")
    
    print("Plotting collaboration between city and citizens...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#ffffff')
    
    # Plot official paths in gray
    official_gdf.plot(ax=ax, color='#bdc3c7', linewidth=1, label='Official Infrastructure')
    
    # Plot desire lines in vibrant orange/red
    user_gdf.plot(ax=ax, color='#e67e22', linewidth=3, alpha=0.8, label='Organic Desire Lines')
    
    ax.set_axis_off()
    ax.set_title('Collaboration: Infrastructure vs. Desire Lines', fontsize=20, pad=20, fontweight='bold')
    ax.legend()
    
    # Add context labels
    ax.text(-122.41, 37.76, 'Usage-Driven', color='#d35400', fontweight='bold')
    ax.text(-122.45, 37.78, 'Planned', color='#7f8c8d', fontweight='bold')
    
    output_path = os.path.join('2024', 'day_17', 'visualization', 'sf_desire_lines.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
