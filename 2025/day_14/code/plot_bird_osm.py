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
    
    # Filter for interesting ones or just plot all
    gdf['centroid'] = gdf.geometry.centroid
    
    print("Plotting birding sites...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')
    
    # Plot SF boundary
    city = ox.geocode_to_gdf(location)
    city.plot(ax=ax, color='#e2e8f0', edgecolor='#94a3b8', linewidth=1)
    
    # Plot bird hides and nests with a vibrant color
    ax.scatter(gdf['centroid'].x, gdf['centroid'].y, color='#0ea5e9', s=50, alpha=0.8, edgecolor='white', linewidth=0.5, label='Birding Point of Interest')
    
    ax.set_axis_off()
    ax.set_title("Day 14: OSM - Birding Infrastructure in SF", fontsize=22, pad=20, fontweight='bold', color='#0369a1')
    
    ax.text(0.5, 0.02, "Data: OpenStreetMap contributors | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=10)
    
    ax.legend(loc='lower left')
    
    output_path = os.path.join('2025', 'day_14', 'visualization', 'sf_birding_osm.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 14: Data challenge: OpenStreetMap
A map of birding-related infrastructure and points of interest in San Francisco, extracted from OpenStreetMap. This includes features tagged as bird hides, observation towers, viewpoints, and known nest sites.

## Visualization
![SF Birding OSM](visualization/sf_birding_osm.png)
"""
    with open(os.path.join('2025', 'day_14', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
