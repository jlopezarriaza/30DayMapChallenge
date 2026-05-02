import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Fetching world boundaries...")
    # Use a reliable GeoJSON source for world boundaries
    url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Projecting to Polar Stereographic (EPSG:3413)...")
    # Arctic Polar Stereographic
    arctic = world.to_crs(epsg=3413)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#f0f8ff') # Alice Blue (icy)
    ax.set_facecolor('#f0f8ff')
    
    # Plot countries
    arctic.plot(ax=ax, color='#ecf0f1', edgecolor='#bdc3c7', linewidth=0.5)
    
    # Focus on the Arctic (center is North Pole)
    # Bounds in EPSG:3413 are large, let's limit to a circle around the pole
    ax.set_xlim(-4000000, 4000000)
    ax.set_ylim(-4000000, 4000000)
    
    # Add a circle for the Arctic Circle (approx 66.5 N)
    # We can't easily draw a perfect circle in projected space without more math, 
    # but we can plot a point at the North Pole.
    ax.scatter([0], [0], color='red', s=50, marker='*', label='North Pole')
    
    ax.set_axis_off()
    ax.set_title('The Arctic Circle', fontsize=24, pad=20, fontweight='bold', color='#2c3e50')
    ax.legend(loc='upper right')
    
    # Add some labels for context
    ax.text(0, -3500000, 'Europe', ha='center', fontsize=12, color='#7f8c8d')
    ax.text(3500000, 0, 'Asia', va='center', fontsize=12, color='#7f8c8d')
    ax.text(-3500000, 0, 'North America', va='center', fontsize=12, color='#7f8c8d')
    
    output_path = os.path.join('2024', 'day_11', 'visualization', 'arctic_map.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#f0f8ff')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
