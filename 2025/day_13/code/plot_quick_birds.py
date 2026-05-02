import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
import osmnx as ox

def main():
    print("Quickly fetching bird sightings in SF...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 212, # Aves
        'limit': 500,
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
    }
    
    resp = requests.get(search_url, params=search_params)
    data = []
    for r in resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude'], 'species': r.get('species', 'Unknown')})
    
    gdf = gpd.GeoDataFrame(pd.DataFrame(data), geometry=gpd.points_from_xy([d['lon'] for d in data], [d['lat'] for d in data]), crs="EPSG:4326")
    
    location = "San Francisco, California, USA"
    print("Fetching base layers for context...")
    # Fetch water and parks for a beautiful basemap
    water = ox.features_from_place(location, tags={'natural': 'water', 'bay': True})
    parks = ox.features_from_place(location, tags={'leisure': 'park'})
    city = ox.geocode_to_gdf(location)
    
    print("Plotting elevated 10-minute map...")
    fig, ax = plt.subplots(figsize=(15, 12))
    fig.patch.set_facecolor('#0f172a') # Deep space navy
    ax.set_facecolor('#0f172a')
    
    # Plot City Base
    city.plot(ax=ax, color='#1e293b', edgecolor='#334155', linewidth=1, zorder=1)
    
    # Plot Water
    water.plot(ax=ax, color='#0284c7', alpha=0.3, zorder=2)
    
    # Plot Parks
    parks.plot(ax=ax, color='#15803d', alpha=0.3, zorder=3)
    
    # Plot top 5 species by count in sample with glowing effect
    top_5 = gdf['species'].value_counts().head(5).index.tolist()
    top_gdf = gdf[gdf['species'].isin(top_5)]
    
    # Glow effect
    top_gdf.plot(ax=ax, column='species', cmap='Set2', markersize=150, alpha=0.2, zorder=4)
    # Core point
    top_gdf.plot(
        ax=ax, 
        column='species', 
        cmap='Set2', 
        markersize=40, 
        alpha=0.9, 
        edgecolor='white',
        linewidth=0.8,
        legend=True,
        legend_kwds={'loc': 'lower left', 'facecolor': '#0f172a', 'edgecolor': '#334155', 'labelcolor': 'white', 'title': 'Top 5 Species', 'title_fontsize': 12},
        zorder=5
    )
    
    # Fix the legend title color
    legend = ax.get_legend()
    if legend:
        legend.get_title().set_color('white')
        legend.get_title().set_fontweight('bold')
    
    # Focus tightly on the SF Peninsula
    ax.set_xlim(-122.52, -122.35)
    ax.set_ylim(37.70, 37.82)
    
    ax.set_axis_off()
    ax.set_title("Day 13: 10 Minute Map - Common SF Birds", color='white', fontsize=28, fontweight='black', pad=20)
    
    output_path = os.path.join('2025', 'day_13', 'visualization', 'sf_common_birds.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f172a')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
