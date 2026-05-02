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
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(10, 10))
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    city.plot(ax=ax, color='#f1f5f9', edgecolor='#cbd5e1')
    
    # Plot top 5 species by count in sample
    top_5 = gdf['species'].value_counts().head(5).index.tolist()
    gdf[gdf['species'].isin(top_5)].plot(ax=ax, column='species', markersize=30, alpha=0.7, legend=True)
    
    ax.set_axis_off()
    ax.set_title("Day 13: 10 Minute Map - Common SF Birds", fontsize=18, fontweight='bold')
    
    output_path = os.path.join('2025', 'day_13', 'visualization', 'sf_common_birds.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 13: 10 minute map
A rapidly generated map showing a sample of the most common bird species found in San Francisco, based on recent GBIF observations. This map was created in under 10 minutes to demonstrate quick spatial data processing.

## Visualization
![SF Common Birds](visualization/sf_common_birds.png)
"""
    with open(os.path.join('2025', 'day_13', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
