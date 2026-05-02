import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching SF major roads for sketchy map...")
    location = "San Francisco, California, USA"
    # Get only major roads to keep the sketch clean
    G = ox.graph_from_place(location, network_type='drive', custom_filter='["highway"~"primary|secondary|tertiary"]')
    
    print("Plotting with XKCD sketchy style...")
    with plt.xkcd():
        fig, ax = ox.plot_graph(
            G, 
            node_size=0, 
            edge_color='black', 
            edge_linewidth=1.5, 
            bgcolor='white',
            show=False, 
            close=False,
            figsize=(12, 12)
        )
        
        ax.set_title('San Francisco (Mostly Accurate)', fontsize=20, pad=20)
        
        # Add some "hand-written" notes
        ax.text(-122.475, 37.81, 'Big Bridge', fontsize=12, color='red')
        ax.text(-122.41, 37.76, 'The Mission', fontsize=12, color='blue')
        ax.text(-122.51, 37.77, 'The Ocean', fontsize=12, color='green')
        
        # Add a note at the bottom
        ax.text(0.5, -0.02, "Drawn by an AI pretending to have hands", 
                transform=ax.transAxes, ha='center', fontsize=10)
        
        output_path = os.path.join('2024', 'day_10', 'visualization', 'sf_sketch.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
