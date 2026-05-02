import osmnx as ox
import matplotlib.pyplot as plt
import os
import geopandas as gpd

def main():
    print("Creating the Grand Finale Map of San Francisco...")
    location = "San Francisco, California, USA"
    
    # 1. Water
    print("Fetching water...")
    water = ox.features_from_place(location, tags={'natural': 'water', 'bay': True, 'waterway': True})
    
    # 2. Parks
    print("Fetching parks...")
    parks = ox.features_from_place(location, tags={'leisure': 'park', 'landuse': 'grass'})
    
    # 3. Roads
    print("Fetching roads...")
    roads = ox.graph_from_place(location, network_type='drive')
    nodes, edges = ox.graph_to_gdfs(roads)
    
    print("Plotting Masterpiece...")
    fig, ax = plt.subplots(figsize=(15, 15))
    fig.patch.set_facecolor('#1a1a1a') # Elegant dark background
    ax.set_facecolor('#1a1a1a')
    
    # Plot Water
    water.plot(ax=ax, color='#1f3a93', alpha=0.8)
    
    # Plot Parks
    parks.plot(ax=ax, color='#27ae60', alpha=0.6)
    
    # Plot Roads (Major)
    major_roads = edges[edges['highway'].isin(['primary', 'secondary', 'tertiary'])]
    major_roads.plot(ax=ax, color='#f1c40f', linewidth=1, alpha=0.8, zorder=10)
    
    # Plot Roads (Minor)
    minor_roads = edges[~edges['highway'].isin(['primary', 'secondary', 'tertiary'])]
    minor_roads.plot(ax=ax, color='#ffffff', linewidth=0.2, alpha=0.3, zorder=5)
    
    # Set the zoom level to SF boundary
    city = ox.geocode_to_gdf(location)
    city_bounds = city.total_bounds # [minx, miny, maxx, maxy]
    ax.set_xlim(city_bounds[0], city_bounds[2])
    ax.set_ylim(city_bounds[1], city_bounds[3])
    
    ax.set_axis_off()
    ax.set_title('San Francisco: The Final Portrait', color='#ffffff', fontsize=32, pad=30, fontweight='black')
    
    # Add a final credit
    ax.text(0.5, 0.01, "#30DayMapChallenge 2024 - Completed by Juan Lopez", 
            transform=ax.transAxes, ha='center', color='#7f8c8d', fontsize=12)
    
    output_path = os.path.join('2024', 'day_30', 'visualization', 'sf_final_masterpiece.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
