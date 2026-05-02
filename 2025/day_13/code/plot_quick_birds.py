import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
import osmnx as ox

def main():
    print("Fetching bird sightings in SF for small multiples...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 212, # Aves
        'limit': 1500, # more data for better distribution
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
    }
    
    resp = requests.get(search_url, params=search_params)
    data = []
    for r in resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude'], 'species': r.get('species', 'Unknown')})
    
    gdf = gpd.GeoDataFrame(pd.DataFrame(data), geometry=gpd.points_from_xy([d['lon'] for d in data], [d['lat'] for d in data]), crs="EPSG:4326")
    
    # Filter out Unknown
    gdf = gdf[gdf['species'] != 'Unknown']
    
    location = "San Francisco, California, USA"
    city = ox.geocode_to_gdf(location)
    
    top_5 = gdf['species'].value_counts().head(5).index.tolist()
    
    print("Plotting small multiples...")
    fig, axes = plt.subplots(1, 5, figsize=(20, 5))
    fig.patch.set_facecolor('#fafaf9') # Off-white
    
    colors = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6']
    
    for i, (species, ax) in enumerate(zip(top_5, axes)):
        ax.set_facecolor('#fafaf9')
        city.plot(ax=ax, color='#e2e8f0', edgecolor='#94a3b8', linewidth=0.5)
        
        species_gdf = gdf[gdf['species'] == species]
        species_gdf.plot(ax=ax, color=colors[i], markersize=15, alpha=0.7)
        
        ax.set_xlim(-122.52, -122.35)
        ax.set_ylim(37.70, 37.82)
        ax.set_axis_off()
        ax.set_title(species, fontsize=14, fontweight='bold', color='#334155', style='italic')
        
    plt.suptitle("Day 13: 10 Minute Map - Small Multiples of Common SF Birds", fontsize=24, fontweight='black', color='#0f172a', y=1.05)
    
    output_path = os.path.join('2025', 'day_13', 'visualization', 'sf_common_birds.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#fafaf9')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
