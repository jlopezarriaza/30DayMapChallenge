import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching SF bike network...")
    # Fetch cycling infrastructure data from OSM for San Francisco
    location = "San Francisco, California, USA"
    # We filter by network_type='bike' which OSMNX handles well
    G = ox.graph_from_place(location, network_type='bike')
    
    print("Plotting...")
    fig, ax = ox.plot_graph(
        G, 
        node_size=0, 
        edge_color='#1f77b4', 
        edge_linewidth=0.5, 
        bgcolor='#111111',
        show=False, 
        close=False
    )
    
    ax.set_title('San Francisco Bike Network', color='white', fontsize=18, pad=20)
    
    # Save the visualization
    output_path = os.path.join('2024', 'day_2', 'visualization', 'sf_bike_network.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#111111')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
