import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
from shapely.geometry import LineString

def main():
    print("Preparing trans-border migration path...")
    # Swainson's Hawk-like path across borders
    # Start: US Great Plains -> Mexico -> Central America -> Colombia -> Argentina
    lons = [-100, -102, -90, -80, -75, -60]
    lats = [45, 25, 15, 8, 2, -35]
    
    path_gdf = gpd.GeoDataFrame({'name': ['Swainson\'s Hawk']}, geometry=[LineString(zip(lons, lats))], crs="EPSG:4326")
    
    print("Fetching political boundaries...")
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
    except:
        pass

    print("Plotting...")
    fig, ax = plt.subplots(figsize=(10, 15))
    fig.patch.set_facecolor('#fdfdfd')
    
    # Plot countries with visible borders
    world.plot(ax=ax, color='#f1f5f9', edgecolor='#94a3b8', linewidth=0.5)
    
    # Plot migration path crossing boundaries
    path_gdf.plot(ax=ax, color='#ef4444', linewidth=3, alpha=0.8, label='Migratory Path')
    
    # Highlight the concept of "Boundaries"
    # We'll label some of the countries crossed
    countries_to_label = ['United States of America', 'Mexico', 'Guatemala', 'Colombia', 'Argentina']
    for country in countries_to_label:
        centroid = world[world['name'] == country].geometry.centroid.iloc[0]
        ax.text(centroid.x, centroid.y, country, fontsize=8, ha='center', color='#475569', alpha=0.7)

    # Focus on the Americas
    ax.set_xlim(-140, -30)
    ax.set_ylim(-60, 60)
    
    ax.set_axis_off()
    ax.set_title("Day 27: Boundaries - Avian Trans-Border Migration", fontsize=24, pad=20, fontweight='bold', color='#0f172a')
    
    ax.text(0.5, 0.05, "Visualizing a single journey across multiple international borders | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=12)
    
    output_path = os.path.join('2025', 'day_27', 'visualization', 'hawk_boundaries.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 27: Boundaries
A map illustrating the trans-border migratory path of a **Swainson's Hawk**. This visualization emphasizes how migratory birds ignore political boundaries as they travel thousands of miles across different nations, highlighting the necessity of international cooperation in wildlife conservation.

## Visualization
![Hawk Boundaries](visualization/hawk_boundaries.png)
"""
    with open(os.path.join('2025', 'day_27', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
