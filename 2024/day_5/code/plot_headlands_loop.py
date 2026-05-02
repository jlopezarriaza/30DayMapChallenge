import osmnx as ox
import matplotlib.pyplot as plt
import os
import networkx as nx

def main():
    print("Fetching route for Headlands Loop...")
    # Define key waypoints for the Headlands Loop
    # Starting near the bridge, going to Hawk Hill, then back via Bunker Rd
    location = "Sausalito, California, USA"
    
    # Get the graph for cycling
    G = ox.graph_from_address("Golden Gate Bridge, San Francisco, CA", dist=5000, network_type='bike')
    
    # Points of interest (lat, lng)
    start_node = ox.nearest_nodes(G, -122.475, 37.808) # Near Presidio
    hawk_hill_node = ox.nearest_nodes(G, -122.499, 37.828) # Hawk Hill
    bunker_rd_node = ox.nearest_nodes(G, -122.503, 37.835) # Near Rodeo Lagoon
    
    # Calculate shortest paths between waypoints
    route1 = nx.shortest_path(G, start_node, hawk_hill_node, weight='length')
    route2 = nx.shortest_path(G, hawk_hill_node, bunker_rd_node, weight='length')
    route3 = nx.shortest_path(G, bunker_rd_node, start_node, weight='length')
    
    combined_route = route1 + route2[1:] + route3[1:]
    
    print("Plotting the journey...")
    fig, ax = ox.plot_graph_route(
        G, combined_route, 
        route_color='red', 
        route_linewidth=3, 
        node_size=0,
        bgcolor='#f0f0f0',
        show=False,
        close=False
    )
    
    ax.set_title('A Journey: The Headlands Loop', fontsize=20, pad=10, fontweight='bold')
    
    # Add labels
    ax.text(-122.475, 37.808, 'Start/End', fontsize=10, color='blue', fontweight='bold')
    ax.text(-122.499, 37.828, 'Hawk Hill', fontsize=10, color='darkred', fontweight='bold')
    
    output_path = os.path.join('2024', 'day_5', 'visualization', 'headlands_loop.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
