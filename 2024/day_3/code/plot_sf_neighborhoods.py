import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Fetching SF neighborhoods data from GitHub...")
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/san-francisco.geojson"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        gdf = gpd.GeoDataFrame.from_features(data['features'])
        gdf.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print(f"Found {len(gdf)} neighborhoods.")
    
    # Project to UTM Zone 10N (EPSG:26910)
    gdf = gdf.to_crs(epsg=26910)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot neighborhoods with a nice colormap
    gdf.plot(
        ax=ax, 
        column='name', 
        cmap='tab20', 
        edgecolor='white', 
        linewidth=0.5,
        alpha=0.8
    )
    
    # Set background color
    fig.patch.set_facecolor('#f5f5f5')
    ax.set_facecolor('#f5f5f5')
    
    # Remove axes
    ax.set_axis_off()
    
    ax.set_title('San Francisco Neighborhoods', fontsize=20, pad=20, fontweight='bold')
    
    # Add labels for neighborhoods
    for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf.name):
        if isinstance(label, str):
            ax.text(x, y, label, fontsize=6, ha='center', alpha=0.7)
    
    # Save the visualization
    output_path = os.path.join('2024', 'day_3', 'visualization', 'sf_neighborhoods.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#f5f5f5')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
