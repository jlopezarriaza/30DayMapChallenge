import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Fetching world map...")
    url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Plotting projections...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 18))
    fig.patch.set_facecolor('#fdfdfd')
    
    # 1. Mercator (Distorts area, preserves angles)
    world_mercator = world.to_crs(epsg=3857)
    world_mercator.plot(ax=ax1, color='#3498db', edgecolor='white', linewidth=0.3)
    ax1.set_title('Mercator Projection (EPSG:3857)', fontsize=20, fontweight='bold')
    ax1.set_axis_off()
    
    # 2. Mollweide (Preserves area, distorts shapes/angles)
    world_mollweide = world.to_crs('+proj=moll')
    world_mollweide.plot(ax=ax2, color='#2ecc71', edgecolor='white', linewidth=0.3)
    ax2.set_title('Mollweide Projection (Equal Area)', fontsize=20, fontweight='bold')
    ax2.set_axis_off()
    
    plt.tight_layout(pad=5.0)
    
    output_path = os.path.join('2024', 'day_26', 'visualization', 'world_projections.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
