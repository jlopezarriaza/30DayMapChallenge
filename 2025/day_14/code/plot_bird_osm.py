import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching bird-related features from OSM in SF...")
    location = "San Francisco, California, USA"
    
    tags = {
        'leisure': 'bird_hide',
        'amenity': 'observation_tower',
        'tourism': 'viewpoint',
        'natural': 'nest'
    }
    
    gdf = ox.features_from_place(location, tags=tags)
    gdf['centroid'] = gdf.geometry.centroid
    
    print("Fetching blueprint base layers...")
    water = ox.features_from_place(location, tags={'natural': 'water', 'bay': True})
    roads = ox.features_from_place(location, tags={'highway': ['primary', 'secondary', 'tertiary']})
    city = ox.geocode_to_gdf(location)
    
    print("Plotting Blueprint style...")
    fig, ax = plt.subplots(figsize=(15, 12))
    # Classic cyan/blue blueprint background
    blueprint_bg = '#0e4f88'
    blueprint_line = '#ffffff'
    fig.patch.set_facecolor(blueprint_bg)
    ax.set_facecolor(blueprint_bg)
    
    # Plot City
    city.plot(ax=ax, color='none', edgecolor=blueprint_line, linewidth=2, zorder=1)
    
    # Plot Water with a hatched pattern to look architectural
    # In matplotlib, hatching works best on solid colors, but we want it transparent. 
    # We can plot with a very low alpha facecolor and a hatched edgecolor.
    water.plot(ax=ax, color=blueprint_bg, edgecolor=blueprint_line, linewidth=0.5, hatch='//////', alpha=0.5, zorder=2)
    
    # Plot Roads
    roads.plot(ax=ax, color=blueprint_line, linewidth=0.3, alpha=0.8, zorder=3)
    
    # Plot POIs in bright yellow
    ax.scatter(gdf['centroid'].x, gdf['centroid'].y, color='#ffd700', s=100, marker='x', linewidths=2, zorder=10, label='Birding Infrastructure')
    ax.scatter(gdf['centroid'].x, gdf['centroid'].y, color='none', edgecolor='#ffd700', s=300, linewidths=1, zorder=10) # Target circle
    
    ax.set_xlim(-122.52, -122.35)
    ax.set_ylim(37.70, 37.82)
    
    ax.set_axis_off()
    ax.set_title("DAY 14: OPENSTREETMAP // BIRDING INFRASTRUCTURE SCHEMATIC", fontsize=24, pad=20, fontweight='black', color=blueprint_line, fontname='monospace')
    
    ax.text(0.5, 0.02, "DATA: OPENSTREETMAP | PROJECT: #30DAYMAPCHALLENGE", 
            transform=ax.transAxes, ha='center', color=blueprint_line, fontsize=12, fontname='monospace', alpha=0.8)
    
    legend = ax.legend(loc='lower left', facecolor=blueprint_bg, edgecolor=blueprint_line, fontsize=12)
    for text in legend.get_texts():
        text.set_color(blueprint_line)
        text.set_fontname('monospace')
    
    output_path = os.path.join('2025', 'day_14', 'visualization', 'sf_birding_osm.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=blueprint_bg)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
