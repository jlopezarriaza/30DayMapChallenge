import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
from shapely.geometry import Polygon

def main():
    print("Fetching world map for speculative future...")
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        data = resp.json()
        world = gpd.GeoDataFrame.from_features(data['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Project to Polar Stereographic for Arctic focus
    arctic = world.to_crs(epsg=3413)
    
    print("Generating speculative 2125 breeding range...")
    # Current range is broad Arctic
    # 2125 range is pushed much closer to the pole, only on high-latitude islands
    future_range = Polygon([
        (0, 80), (45, 82), (90, 85), (135, 82), (180, 80), (-135, 82), (-90, 85), (-45, 82), (0, 80)
    ])
    range_gdf = gpd.GeoDataFrame({'name': ['Arctic Tern 2125']}, geometry=[future_range], crs="EPSG:4326").to_crs(epsg=3413)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    # Plot countries (as they might look with higher sea levels? let's keep simple for now)
    arctic.plot(ax=ax, color='#1e293b', edgecolor='#334155', linewidth=0.5)
    
    # Plot future range in a "warning" color
    range_gdf.plot(ax=ax, color='#fde047', alpha=0.5, edgecolor='#eab308', linewidth=1, hatch='///', label='Breeding Range (Speculative)')
    
    # Focus tight on the Pole
    ax.set_xlim(-3000000, 3000000)
    ax.set_ylim(-3000000, 3000000)
    
    ax.set_axis_off()
    ax.set_title("Status of the Arctic Tern (Larus paradisaea) - Year 2125", color='white', fontsize=22, pad=20, fontweight='bold')
    
    ax.text(0.5, 0.05, "Archival Map retrieved from Global Climate Museum | Project: #30DayMapChallenge", 
            transform=ax.transAxes, ha='center', color='#94a3b8', fontsize=10, style='italic')
    
    output_path = os.path.join('2025', 'day_12', 'visualization', 'arctic_tern_2125.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f172a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 12: Map from 2125
A speculative "historical" map from the year 2125, visualizing the drastically reduced breeding range of the Arctic Tern. As the Arctic warms, this species is forced into a narrow and fragmented band around the high-latitude islands near the North Pole.

## Visualization
![Arctic Tern 2125](visualization/arctic_tern_2125.png)
"""
    with open(os.path.join('2025', 'day_12', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
