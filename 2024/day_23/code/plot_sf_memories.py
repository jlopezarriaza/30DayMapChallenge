import matplotlib.pyplot as plt
import os
import geopandas as gpd
from shapely.geometry import Point

def main():
    # Define some "Memory" points in SF
    memories = {
        'Mission Dolores': (-122.427, 37.764),
        'Coit Tower': (-122.406, 37.802),
        'Golden Gate Bridge': (-122.478, 37.819),
        'The Ferry Building': (-122.393, 37.795),
        'Painted Ladies': (-122.433, 37.776),
        'Twin Peaks': (-122.447, 37.754),
        'Oracle Park': (-122.389, 37.778)
    }
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {'name': list(memories.keys())},
        geometry=[Point(lon, lat) for lon, lat in memories.values()],
        crs="EPSG:4326"
    )
    
    print("Plotting memory map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#fffcf0') # Warm cream
    ax.set_facecolor('#fffcf0')
    
    # Plot SF boundary for context
    import osmnx as ox
    location = "San Francisco, California, USA"
    city = ox.geocode_to_gdf(location)
    city.plot(ax=ax, color='#f5e6d3', edgecolor='#d4b483', alpha=0.5)
    
    # Plot memory points
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='#c0392b', s=100, marker='o', alpha=0.8)
    
    # Add labels with a "handwritten" feel
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.name):
        ax.text(x + 0.002, y + 0.002, label, fontsize=12, fontname='serif', fontstyle='italic')
    
    ax.set_axis_off()
    ax.set_title('San Francisco: A Map of Memories', fontsize=24, pad=20, fontname='serif', fontweight='bold', color='#4a3728')
    
    output_path = os.path.join('2024', 'day_23', 'visualization', 'sf_memories.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#fffcf0')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
