import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
from shapely.geometry import Point

def main():
    # List of some US places named after birds
    places = [
        {'name': 'Phoenix, AZ', 'lat': 33.448, 'lon': -112.074, 'bird': 'Phoenix'},
        {'name': 'Eagle, ID', 'lat': 43.695, 'lon': -116.353, 'bird': 'Eagle'},
        {'name': 'Falcon, CO', 'lat': 38.928, 'lon': -104.607, 'bird': 'Falcon'},
        {'name': 'Pelican, AK', 'lat': 57.958, 'lon': -136.223, 'bird': 'Pelican'},
        {'name': 'Larkspur, CA', 'lat': 37.934, 'lon': -122.535, 'bird': 'Lark'},
        {'name': 'Swansea, MA', 'lat': 41.745, 'lon': -71.189, 'bird': 'Swan'},
        {'name': 'Ravenna, OH', 'lat': 41.157, 'lon': -81.242, 'bird': 'Raven'},
        {'name': 'Bluebird, KY', 'lat': 37.5, 'lon': -84.5, 'bird': 'Bluebird'}, # Approx
        {'name': 'Cardinal, VA', 'lat': 37.4, 'lon': -76.3, 'bird': 'Cardinal'}, # Approx
        {'name': 'Heron Lake, MN', 'lat': 43.793, 'lon': -95.319, 'bird': 'Heron'},
        {'name': 'Robins, IA', 'lat': 42.062, 'lon': -91.669, 'bird': 'Robin'},
        {'name': 'Osprey, FL', 'lat': 27.192, 'lon': -82.491, 'bird': 'Osprey'},
    ]
    
    df = pd.DataFrame(places)
    gdf = gpd.GeoDataFrame(df, geometry=[Point(p['lon'], p['lat']) for p in places], crs="EPSG:4326")
    
    print("Plotting avian toponyms...")
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#fdfdfd')
    
    # Plot US boundary
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        usa = world[world['name'] == 'United States of America']
        usa.plot(ax=ax, color='#f1f5f9', edgecolor='#cbd5e1', linewidth=1)
    except:
        pass
    
    # Plot places with bird-themed colors
    gdf.plot(ax=ax, color='#1e293b', markersize=80, edgecolor='white', linewidth=1)
    
    # Add labels
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.name):
        ax.text(x + 0.5, y + 0.2, label, fontsize=10, fontweight='bold', color='#1e293b')
    
    # Focus on lower 48 (mostly)
    ax.set_xlim(-125, -67)
    ax.set_ylim(24, 50)
    
    ax.set_axis_off()
    ax.set_title("Day 24: Places and Names - Avian Toponyms across the US", fontsize=24, pad=20, fontweight='bold')
    
    ax.text(0.5, 0.05, "Mapping towns and cities named after birds | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=12)
    
    output_path = os.path.join('2025', 'day_24', 'visualization', 'avian_toponyms.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 24: Places and their names
A map of towns and cities across the United States named after birds (toponyms). From Eagle, Idaho to Osprey, Florida, this visualization explores how avian species have left their mark on our geographic naming conventions.

## Visualization
![Avian Toponyms](visualization/avian_toponyms.png)
"""
    with open(os.path.join('2025', 'day_24', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
