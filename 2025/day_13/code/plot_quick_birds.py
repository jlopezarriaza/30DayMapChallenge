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
    top_5 = gdf['species'].value_counts().head(5).index.tolist()
    
    print("Fetching base layers...")
    bbox = (-122.52, 37.70, -122.35, 37.82)
    # Fetch roads and water
    water = ox.features_from_bbox(bbox, tags={'natural': 'water', 'bay': True})
    roads = ox.features_from_bbox(bbox, tags={'highway': ['primary', 'secondary']})
    
    print("Plotting small multiples...")
    fig, axes = plt.subplots(1, 5, figsize=(25, 6))
    bg_color = '#0f172a' # Dark navy
    fig.patch.set_facecolor(bg_color)
    
    colors = ['#f43f5e', '#f59e0b', '#10b981', '#38bdf8', '#8b5cf6']
    
    for i, (species, ax) in enumerate(zip(top_5, axes)):
        ax.set_facecolor(bg_color)
        
        # Plot roads and water
        roads.plot(ax=ax, color='#1e293b', linewidth=0.5, alpha=0.8)
        water.plot(ax=ax, color='#0284c7', alpha=0.2)
        
        species_gdf = gdf[gdf['species'] == species]
        
        # Glow
        species_gdf.plot(ax=ax, color=colors[i], markersize=100, alpha=0.2)
        # Core
        species_gdf.plot(ax=ax, color=colors[i], markersize=15, alpha=0.9, edgecolor='white', linewidth=0.5)
        
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])
        ax.set_axis_off()
        ax.set_title(species, fontsize=16, fontweight='bold', color='white', style='italic', pad=15)
        
    plt.suptitle("Day 13: 10 Minute Map - Common SF Birds", fontsize=28, fontweight='black', color='white', y=1.05)
    
    output_path = os.path.join('2025', 'day_13', 'visualization', 'sf_common_birds.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=bg_color)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
