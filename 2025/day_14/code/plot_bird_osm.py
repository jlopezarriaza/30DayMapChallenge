import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching bird-related features from OSM in SF...")
    location = "San Francisco, California, USA"
    
    # Common tags for birding related features
    tags = {
        'leisure': 'bird_hide',
        'amenity': 'observation_tower',
        'tourism': 'viewpoint',
        'natural': 'nest'
    }
    
    gdf = ox.features_from_place(location, tags=tags)
    print(f"Found {len(gdf)} bird-related features.")
    
    # Get centroids
    gdf['centroid'] = gdf.geometry.centroid
    
    print("Fetching rich base layers...")
    water = ox.features_from_place(location, tags={'natural': 'water', 'bay': True})
    parks = ox.features_from_place(location, tags={'leisure': 'park'})
    roads = ox.features_from_place(location, tags={'highway': ['primary', 'secondary']})
    city = ox.geocode_to_gdf(location)
    
    print("Plotting high-fidelity birding sites...")
    fig, ax = plt.subplots(figsize=(15, 12))
    fig.patch.set_facecolor('#020617') # Very dark blue/black
    ax.set_facecolor('#020617')
    
    # Plot SF boundary
    city.plot(ax=ax, color='#0f172a', edgecolor='#1e293b', linewidth=1.5, zorder=1)
    
    # Plot Water
    water.plot(ax=ax, color='#0369a1', alpha=0.4, zorder=2)
    
    # Plot Parks
    parks.plot(ax=ax, color='#065f46', alpha=0.3, zorder=3)
    
    # Plot Roads
    roads.plot(ax=ax, color='#334155', linewidth=0.5, alpha=0.5, zorder=4)
    
    # Plot bird hides and nests with a vibrant cyan color
    # Outer glow
    ax.scatter(gdf['centroid'].x, gdf['centroid'].y, color='#22d3ee', s=200, alpha=0.2, zorder=10)
    # Inner point
    ax.scatter(gdf['centroid'].x, gdf['centroid'].y, color='#38bdf8', s=50, alpha=0.9, edgecolor='white', linewidth=1, label='Birding POI', zorder=11)
    
    # Focus tightly on the SF Peninsula, ignoring the Farallon Islands
    ax.set_xlim(-122.52, -122.35)
    ax.set_ylim(37.70, 37.82)
    
    ax.set_axis_off()
    ax.set_title("Day 14: OSM - Birding Infrastructure in SF", fontsize=28, pad=20, fontweight='black', color='#38bdf8')
    
    ax.text(0.5, 0.02, "Data: OpenStreetMap contributors | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#94a3b8', fontsize=12)
    
    # Customize legend for dark background
    legend = ax.legend(loc='lower left', facecolor='#0f172a', edgecolor='#334155', fontsize=12)
    for text in legend.get_texts():
        text.set_color('#f8fafc')
    
    output_path = os.path.join('2025', 'day_14', 'visualization', 'sf_birding_osm.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#020617')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
