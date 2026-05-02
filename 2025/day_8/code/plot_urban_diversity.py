import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
import osmnx as ox

def main():
    print("Fetching SF neighborhood boundaries...")
    url_hoods = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/san-francisco.geojson"
    try:
        resp = requests.get(url_hoods)
        hoods_gdf = gpd.GeoDataFrame.from_features(resp.json()['features'])
        hoods_gdf.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error fetching neighborhoods: {e}")
        return

    print("Fetching bird species sightings in SF...")
    # Class 'Aves' Key: 212
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 212,
        'limit': 1000,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
    }
    
    search_resp = requests.get(search_url, params=search_params)
    sightings = search_resp.json()
    
    data = []
    for r in sightings['results']:
        data.append({
            'lat': r['decimalLatitude'],
            'lon': r['decimalLongitude'],
            'species': r.get('species', 'Unknown')
        })
    sightings_df = pd.DataFrame(data)
    sightings_gdf = gpd.GeoDataFrame(sightings_df, geometry=gpd.points_from_xy(sightings_df.lon, sightings_df.lat), crs="EPSG:4326")
    
    print("Aggregating species diversity by neighborhood...")
    # Spatial join
    joined = gpd.sjoin(sightings_gdf, hoods_gdf, how="inner", predicate="within")
    
    # Count unique species per neighborhood
    diversity = joined.groupby('name')['species'].nunique().reset_index()
    diversity.columns = ['name', 'species_count']
    
    # Join back to neighborhoods
    hoods_gdf = hoods_gdf.merge(diversity, on='name', how='left').fillna(0)
    
    print("Plotting urban bird diversity...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#fdfdfd')
    
    hoods_gdf.plot(
        ax=ax, 
        column='species_count', 
        cmap='YlGn', 
        edgecolor='#444444', 
        linewidth=0.5,
        legend=True,
        legend_kwds={'label': "Unique Bird Species Count (Sample)", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    ax.set_axis_off()
    ax.set_title("Day 8: Urban - Bird Diversity in SF Neighborhoods", fontsize=22, pad=20, fontweight='bold', color='#166534')
    
    ax.text(0.5, 0.02, "Data: GBIF & Code for America | Theme: Birds | World Urbanism Day", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=10)
    
    output_path = os.path.join('2025', 'day_8', 'visualization', 'sf_urban_bird_diversity.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 8: Urban
A choropleth map showing the diversity of bird species found in different San Francisco neighborhoods. This visualization highlights the richness of urban biodiversity, calculated by counting unique species sightings from a sample of GBIF data within each administrative boundary.

## Visualization
![SF Urban Bird Diversity](visualization/sf_urban_bird_diversity.png)
"""
    with open(os.path.join('2025', 'day_8', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
