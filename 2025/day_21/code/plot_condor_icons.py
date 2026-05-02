import matplotlib.pyplot as plt
import os
import geopandas as gpd
from shapely.geometry import Point
import osmnx as ox
import requests

def main():
    # Known recovery/release/sighting areas for California Condor
    sites = [
        {'name': 'Pinnacles National Park', 'lat': 36.49, 'lon': -121.18},
        {'name': 'Big Sur Coast', 'lat': 36.27, 'lon': -121.81},
        {'name': 'Bitter Creek NWR', 'lat': 34.85, 'lon': -119.38},
        {'name': 'Hopper Mountain NWR', 'lat': 34.45, 'lon': -118.85},
        {'name': 'Vermilion Cliffs', 'lat': 36.86, 'lon': -111.75},
        {'name': 'Zion National Park', 'lat': 37.30, 'lon': -113.05}
    ]
    
    df = gpd.GeoDataFrame(sites, geometry=[Point(s['lon'], s['lat']) for s in sites], crs="EPSG:4326")
    
    print("Plotting with icons...")
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#fdfdfd')
    
    # Plot West US boundary
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        resp.raise_for_status()
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
        usa = world[world['name'] == 'United States of America']
        usa.plot(ax=ax, color='#f1f5f9', edgecolor='#cbd5e1', linewidth=1)
    except Exception as e:
        print(f"Error fetching background: {e}")
    
    # Plot icons (we'll use a specific marker and label)
    # Using a custom 'V' shape marker for a bird in flight
    ax.scatter(df.geometry.x, df.geometry.y, marker='v', color='#1e293b', s=200, label='Condor Site')
    
    # Add labels
    for x, y, label in zip(df.geometry.x, df.geometry.y, df.name):
        ax.text(x + 0.2, y + 0.2, label, fontsize=12, fontweight='bold', color='#475569')
    
    # Focus on SW US
    ax.set_xlim(-125, -110)
    ax.set_ylim(32, 40)
    
    ax.set_axis_off()
    ax.set_title("Day 21: Icons - California Condor Recovery Sites", fontsize=24, pad=20, fontweight='bold', color='#0f172a')
    
    output_path = os.path.join('2025', 'day_21', 'visualization', 'condor_icons.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 21: Icons
A map of critical recovery and release sites for the **California Condor** (*Gymnogyps californianus*). The map uses stylized markers to denote key locations in California and Arizona where these birds have been reintroduced to the wild.

## Visualization
![Condor Icons](visualization/condor_icons.png)
"""
    with open(os.path.join('2025', 'day_21', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
