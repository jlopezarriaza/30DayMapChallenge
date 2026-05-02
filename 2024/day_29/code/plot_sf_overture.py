import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching SF building footprints...")
    # Focus on a dense area: North Beach / Telegraph Hill
    center = (37.80, -122.41)
    tags = {'building': True}
    gdf = ox.features_from_point(center, tags=tags, dist=800)
    
    print("Plotting Overture-style urban fabric...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#fdfdfd')
    ax.set_facecolor('#fdfdfd')
    
    # Plot buildings with a clean, semi-transparent look
    gdf.plot(ax=ax, color='#2c3e50', edgecolor='white', linewidth=0.3, alpha=0.9)
    
    # Plot roads for context (faint)
    roads = ox.features_from_point(center, tags={'highway': True}, dist=800)
    roads.plot(ax=ax, color='#ecf0f1', linewidth=1, alpha=0.5, zorder=0)
    
    ax.set_axis_off()
    ax.set_title('Urban Fabric: San Francisco (Overture-Style)', fontsize=24, pad=20, fontweight='bold', color='#2c3e50')
    
    output_path = os.path.join('2024', 'day_29', 'visualization', 'sf_urban_fabric.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
