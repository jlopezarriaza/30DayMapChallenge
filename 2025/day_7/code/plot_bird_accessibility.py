import osmnx as ox
import matplotlib.pyplot as plt
import os
import geopandas as gpd
from shapely.geometry import Point

def main():
    print("Fetching SF transit hubs and birding spots (parks/reserves)...")
    location = "San Francisco, California, USA"
    
    # 1. Transit Hubs (BART/MUNI stations)
    transit_tags = {'railway': 'station', 'public_transport': 'station'}
    transit_gdf = ox.features_from_place(location, tags=transit_tags)
    transit_gdf['centroid'] = transit_gdf.geometry.centroid
    
    # 2. Birding Spots (Parks and Nature Reserves)
    birding_tags = {'leisure': 'park', 'boundary': 'nature_reserve'}
    birding_gdf = ox.features_from_place(location, tags=birding_tags)
    birding_gdf['centroid'] = birding_gdf.geometry.centroid
    
    print(f"Found {len(transit_gdf)} transit hubs and {len(birding_gdf)} potential birding spots.")
    
    # Project to a local CRS for distance calculation (UTM 10N)
    transit_gdf = transit_gdf.to_crs(epsg=26910)
    birding_gdf = birding_gdf.to_crs(epsg=26910)
    
    print("Calculating accessibility (proximity)...")
    # For each birding spot, find distance to nearest transit hub
    def min_dist(point, others):
        return others.distance(point).min()
        
    birding_gdf['dist_to_transit'] = birding_gdf['centroid'].to_crs(epsg=26910).apply(lambda p: min_dist(p, transit_gdf['centroid']))
    
    print("Plotting accessibility map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#fdfdfd')
    
    # Plot SF boundary
    city = ox.geocode_to_gdf(location).to_crs(epsg=26910)
    city.plot(ax=ax, color='#f1f5f9', edgecolor='#cbd5e1', linewidth=1)
    
    # Plot birding spots colored by accessibility (closer is better)
    birding_gdf.plot(
        ax=ax, 
        column='dist_to_transit', 
        cmap='RdYlGn_r', # Red for far, Green for close
        legend=True,
        legend_kwds={'label': "Distance to Nearest Transit Hub (meters)", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    # Plot transit hubs as points
    transit_gdf.plot(ax=ax, color='blue', markersize=10, alpha=0.5, label='Transit Hub')
    
    ax.set_axis_off()
    ax.set_title("Day 7: Accessibility - Urban Birding Proximity in SF", fontsize=22, pad=20, fontweight='bold')
    
    output_path = os.path.join('2025', 'day_7', 'visualization', 'sf_birding_accessibility.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 7: Accessibility
A map analyzing the accessibility of birding spots (parks and nature reserves) in San Francisco relative to major transit hubs (BART and MUNI stations). Regions in green are within easy walking distance of a station, promoting car-free urban birding.

## Visualization
![SF Birding Accessibility](visualization/sf_birding_accessibility.png)
"""
    with open(os.path.join('2025', 'day_7', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
