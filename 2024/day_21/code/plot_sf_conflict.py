import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching SF road network...")
    location = "San Francisco, California, USA"
    G = ox.graph_from_place(location, network_type='drive')
    
    # Convert graph to GeoDataFrames
    nodes, edges = ox.graph_to_gdfs(G)
    
    # Identify the Great Highway
    # In OSM, name is usually 'Great Highway'
    great_highway = edges[edges['name'].str.contains('Great Highway', na=False)]
    
    print(f"Found {len(great_highway)} segments of the Great Highway.")
    
    print("Plotting conflict map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#fdfdfd')
    ax.set_facecolor('#fdfdfd')
    
    # Plot all edges in a neutral light gray
    edges.plot(ax=ax, color='#e0e0e0', linewidth=0.5, alpha=0.5)
    
    # Plot Great Highway in bold red to represent conflict/tension
    great_highway.plot(ax=ax, color='#e74c3c', linewidth=3, label='Great Highway (Park vs. Road)')
    
    ax.set_axis_off()
    ax.set_title('Urban Conflict: The Great Highway, SF', fontsize=24, pad=20, fontweight='bold', color='#2c3e50')
    
    # Add an explanatory note
    ax.text(0.5, 0.05, "Highlighting the stretch at the center of the road-to-park transition debate.", 
            transform=ax.transAxes, ha='center', fontsize=12, color='#34495e', style='italic')
    
    ax.legend(loc='upper left', frameon=True, facecolor='white')
    
    output_path = os.path.join('2024', 'day_21', 'visualization', 'sf_great_highway_conflict.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
