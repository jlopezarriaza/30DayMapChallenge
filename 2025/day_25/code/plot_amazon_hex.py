import pandas as pd
import h3
import matplotlib.pyplot as plt
import requests
import os
import geopandas as gpd
from shapely.geometry import Polygon

def main():
    print("Fetching Amazon bird sightings for hexagonal richness map...")
    # Bounds for Amazon basin approx: -80 to -45 Lon, -20 to 10 Lat
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 212, # Aves
        'limit': 1000,
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-80 -20, -45 -20, -45 10, -80 10, -80 -20))'
    }
    
    resp = requests.get(search_url, params=search_params)
    data = []
    for r in resp.json()['results']:
        data.append({
            'lat': r['decimalLatitude'], 
            'lon': r['decimalLongitude'], 
            'species': r.get('species', 'Unknown')
        })
    df = pd.DataFrame(data)
    
    print("Binning into H3 hexagons...")
    resolution = 5 # Larger resolution for continental scale
    df['h3_cell'] = df.apply(lambda row: h3.latlng_to_cell(row['lat'], row['lon'], resolution), axis=1)
    
    # Count unique species per cell
    richness = df.groupby('h3_cell')['species'].nunique().reset_index()
    richness.columns = ['h3_cell', 'species_count']
    
    # Convert to polygons
    def cell_to_polygon(cell):
        boundary = h3.cell_to_boundary(cell)
        return Polygon([(lng, lat) for lat, lng in boundary])
    
    richness['geometry'] = richness['h3_cell'].apply(cell_to_polygon)
    gdf = gpd.GeoDataFrame(richness, geometry='geometry', crs="EPSG:4326")
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(15, 12))
    fig.patch.set_facecolor('#052e16') # Dark forest green
    ax.set_facecolor('#052e16')
    
    # Plot South America boundary (subtle)
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        world_resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(world_resp.json()['features'])
        world.plot(ax=ax, color='#064e3b', edgecolor='#065f46', linewidth=0.5, alpha=0.5)
    except:
        pass
    
    # Plot richness hexagons
    gdf.plot(
        ax=ax, 
        column='species_count', 
        cmap='Greens', 
        edgecolor='#14532d', 
        linewidth=0.5,
        legend=True,
        legend_kwds={'label': "Unique Species Count per Hexagon", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    # Focus on the Amazon
    ax.set_xlim(-85, -40)
    ax.set_ylim(-25, 15)
    
    ax.set_axis_off()
    ax.set_title("Day 25: Hexagons - Bird Species Richness in the Amazon", color='white', fontsize=24, pad=20, fontweight='bold')
    
    ax.text(0.5, 0.02, "Data: GBIF Sample | Theme: Birds | Binning: H3 Resolution 5", 
            transform=ax.transAxes, ha='center', color='#d1fae5', fontsize=12)
    
    output_path = os.path.join('2025', 'day_25', 'visualization', 'amazon_bird_hexagons.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#052e16')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 25: Hexagons
A hexagonal binning map visualizing bird species richness in the Amazon Rainforest. Using the H3 spatial index, a broad sample of sightings is aggregated into regular hexagons, revealing high-biodiversity "hotspots" within the basin.

## Visualization
![Amazon Bird Hexagons](visualization/amazon_bird_hexagons.png)
"""
    with open(os.path.join('2025', 'day_25', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
