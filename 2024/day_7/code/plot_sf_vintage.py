import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching SF road network for vintage map...")
    location = "San Francisco, California, USA"
    # Fetch major and minor roads
    G = ox.graph_from_place(location, network_type='drive')
    
    print("Plotting with vintage aesthetic...")
    # Background color: parchment-like
    bg_color = '#F5E6D3'
    # Road colors: sepia / dark brown
    road_color = '#4A3728'
    
    fig, ax = ox.plot_graph(
        G, 
        node_size=0, 
        edge_color=road_color, 
        edge_linewidth=0.3, 
        bgcolor=bg_color,
        show=False, 
        close=False,
        figsize=(12, 12)
    )
    
    # Add a decorative title
    ax.set_title('San Francisco, California', 
                 color='#2F1E0E', 
                 fontsize=28, 
                 fontname='serif', 
                 fontstyle='italic',
                 pad=20)
    
    # Add a border
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('#2F1E0E')
        spine.set_linewidth(2)
        
    # Add a "label" at the bottom
    ax.text(0.5, -0.05, "Anno MMXXIV - #30DayMapChallenge", 
            transform=ax.transAxes, 
            ha='center', 
            fontsize=12, 
            color='#2F1E0E', 
            fontname='serif')
    
    output_path = os.path.join('2024', 'day_7', 'visualization', 'sf_vintage.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=bg_color)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
