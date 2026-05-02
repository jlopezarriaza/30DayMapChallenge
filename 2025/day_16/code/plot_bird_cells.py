import pandas as pd
import h3
import matplotlib.pyplot as plt
import requests
import os
import geopandas as gpd
from shapely.geometry import Polygon

def main():
    print("Fetching bird sightings in SF for H3 binning...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 212,
        'limit': 1000,
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
    }
    
    resp = requests.get(search_url, params=search_params)
    data = []
    for r in resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    df = pd.DataFrame(data)
    
    print("Binning into H3 cells...")
    resolution = 9
    df['h3_cell'] = df.apply(lambda row: h3.latlng_to_cell(row['lat'], row['lon'], resolution), axis=1)
    
    # Count sightings per cell
    counts = df['h3_cell'].value_counts().reset_index()
    counts.columns = ['h3_cell', 'sighting_count']
    
    # Convert to polygons
    def cell_to_polygon(cell):
        boundary = h3.cell_to_boundary(cell)
        return Polygon([(lng, lat) for lat, lng in boundary])
    
    counts['geometry'] = counts['h3_cell'].apply(cell_to_polygon)
    gdf = gpd.GeoDataFrame(counts, geometry='geometry', crs="EPSG:4326")
    
    print("Plotting cell map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    # Plot SF boundary
    import osmnx as ox
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    city.plot(ax=ax, color='#1e293b', edgecolor='#334155', linewidth=1)
    
    # Plot cells
    gdf.plot(
        ax=ax, 
        column='sighting_count', 
        cmap='YlOrRd', 
        edgecolor='none', 
        alpha=0.8,
        legend=True,
        legend_kwds={'label': "Sighting Density per H3 Cell", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    ax.set_axis_off()
    ax.set_title("Day 16: Cell - Bird Sighting Density (H3) in SF", color='white', fontsize=22, pad=20, fontweight='bold')
    
    output_path = os.path.join('2025', 'day_16', 'visualization', 'sf_bird_h3_cells.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f172a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 16: Cell
A visualization of bird sighting density in San Francisco, binned into hexagonal **H3 Cells** (resolution 9). This map abstracts thousands of individual observation points into a regular grid, highlighting the most active "cells" for urban birdwatching.

## Visualization
![SF Bird H3 Cells](visualization/sf_bird_h3_cells.png)
"""
    with open(os.path.join('2025', 'day_16', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
