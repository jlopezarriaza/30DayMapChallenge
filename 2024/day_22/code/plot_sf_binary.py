import osmnx as ox
import matplotlib.pyplot as plt
import os
import geopandas as gpd

def main():
    print("Fetching SF boundary...")
    location = "San Francisco, California, USA"
    city = ox.geocode_to_gdf(location)
    
    print("Plotting binary map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    # Background: White (represents water)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Land: Black
    city.plot(ax=ax, color='black', edgecolor='none')
    
    ax.set_axis_off()
    ax.set_title('San Francisco: Two Colours', color='black', fontsize=24, pad=20, fontweight='bold')
    
    output_path = os.path.join('2024', 'day_22', 'visualization', 'sf_binary.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
