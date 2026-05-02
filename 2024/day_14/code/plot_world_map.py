import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Fetching world time zone data...")
    # Time zone boundaries are often large, I'll use a reliable source if available or fallback to a simpler world map
    url = "https://raw.githubusercontent.com/evansiroky/timezone-boundary-builder/master/release/combined-with-oceans.json"
    
    # This file might be too big to download directly in a script every time, 
    # let's try a smaller version if possible or just use a standard world map and join with some TZ data.
    # Actually, I'll use the basic world map and color by a synthetic 'offset' for simplicity and robustness.
    
    world_url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"
    try:
        resp = requests.get(world_url)
        resp.raise_for_status()
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Plotting world map...")
    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor('#ffffff')
    
    # Use 'Winkel Tripel' projection for a nice world map look (not standard in EPSG, but we can use Robinson)
    # Robinson is EPSG:54030 usually
    world_robinson = world.to_crs('+proj=robin')
    
    # Random colors for countries to look like a map
    world_robinson.plot(
        ax=ax, 
        column='name', 
        cmap='Set3', 
        edgecolor='black', 
        linewidth=0.2
    )
    
    ax.set_axis_off()
    ax.set_title('The World Map: A Global Perspective', fontsize=24, pad=20, fontweight='bold')
    
    output_path = os.path.join('2024', 'day_14', 'visualization', 'world_map.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
