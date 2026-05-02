import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Micromapping Salesforce Tower area...")
    center = (37.7897, -122.3972) # Salesforce Tower
    
    # Fetch buildings
    buildings = ox.features_from_point(center, tags={'building': True}, dist=200)
    
    # Fetch footways/paths
    paths = ox.features_from_point(center, tags={'highway': ['footway', 'pedestrian', 'path']}, dist=200)
    
    # Fetch parks/leisure
    parks = ox.features_from_point(center, tags={'leisure': 'park'}, dist=200)
    
    print("Plotting detailed map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#ffffff')
    
    # Plot buildings
    buildings.plot(ax=ax, color='#34495e', edgecolor='#2c3e50', linewidth=0.5, alpha=0.8)
    
    # Plot paths
    paths.plot(ax=ax, color='#bdc3c7', linewidth=2, linestyle='--')
    
    # Plot parks
    if not parks.empty:
        parks.plot(ax=ax, color='#2ecc71', alpha=0.5)
    
    # Focus tight on the area
    ax.set_xlim(center[1] - 0.002, center[1] + 0.002)
    ax.set_ylim(center[0] - 0.002, center[0] + 0.002)
    
    # Highlight Salesforce Tower
    tower = buildings[buildings['name'] == 'Salesforce Tower']
    if not tower.empty:
        tower.plot(ax=ax, color='#2980b9', edgecolor='#1f3a93', linewidth=2)
        ax.text(center[1], center[0] + 0.0002, 'Salesforce Tower', 
                ha='center', fontsize=14, fontweight='bold', color='#2980b9')
    
    ax.set_axis_off()
    ax.set_title('Micromapping: Salesforce Tower & Surroundings', fontsize=22, pad=20, fontweight='bold')
    
    output_path = os.path.join('2024', 'day_27', 'visualization', 'sf_micromap.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
