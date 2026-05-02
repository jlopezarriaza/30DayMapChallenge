import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching SF water features...")
    location = "San Francisco, California, USA"
    # Fetch water bodies, rivers, and the bay coastline
    tags = {'natural': 'water', 'waterway': True, 'bay': True}
    gdf = ox.features_from_place(location, tags=tags)
    
    print("Plotting the blue planet map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0b0e14')
    ax.set_facecolor('#0b0e14')
    
    # Plot water in various shades of blue
    gdf.plot(ax=ax, color='#1e90ff', alpha=0.6, edgecolor='#00bfff', linewidth=0.5)
    
    # Add a title
    ax.set_axis_off()
    ax.set_title('The Blue Planet: San Francisco Bay & Waterways', 
                 color='#1e90ff', fontsize=24, pad=20, fontweight='bold')
    
    # Add a glowing effect by plotting again with more alpha and smaller linewidth
    gdf.plot(ax=ax, color='#00bfff', alpha=0.2, linewidth=2)
    
    output_path = os.path.join('2024', 'day_28', 'visualization', 'sf_blue_planet.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0b0e14')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
