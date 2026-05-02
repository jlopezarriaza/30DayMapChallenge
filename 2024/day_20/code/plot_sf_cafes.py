import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching cafes in SF from OpenStreetMap...")
    location = "San Francisco, California, USA"
    tags = {'amenity': 'cafe'}
    gdf = ox.features_from_place(location, tags=tags)
    
    # Filter for points (some might be polygons)
    gdf['centroid'] = gdf.geometry.centroid
    
    print(f"Found {len(gdf)} cafes.")
    
    print("Plotting coffee map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#2c2c2c')
    ax.set_facecolor('#2c2c2c')
    
    # Plot SF boundary for context
    city = ox.geocode_to_gdf(location)
    city.plot(ax=ax, color='#1e1e1e', edgecolor='#444444', linewidth=1)
    
    # Plot cafes as glowing points
    ax.scatter(
        gdf['centroid'].x, 
        gdf['centroid'].y, 
        s=15, 
        color='#f39c12', 
        alpha=0.8, 
        edgecolor='white', 
        linewidth=0.2,
        label='Cafe'
    )
    
    ax.set_axis_off()
    ax.set_title('Caffeine Culture: San Francisco Cafes', color='#f39c12', fontsize=22, pad=20, fontweight='bold')
    
    # Add OSM credit
    ax.text(0.99, 0.01, '© OpenStreetMap contributors', transform=ax.transAxes, 
            ha='right', va='bottom', color='#7f8c8d', fontsize=8)
    
    output_path = os.path.join('2024', 'day_20', 'visualization', 'sf_cafes.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#2c2c2c')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
