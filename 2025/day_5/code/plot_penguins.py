import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Finding Penguin family (Spheniscidae) in GBIF...")
    family_name = "Spheniscidae"
    match_url = "https://api.gbif.org/v1/species/match"
    match_params = {'name': family_name, 'rank': 'FAMILY'}
    
    match_resp = requests.get(match_url, params=match_params)
    match_resp.raise_for_status()
    family_key = match_resp.json()['usageKey']
    
    print(f"Fetching sightings for {family_name} (Key: {family_key}) globally...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    # Fetch a large-ish sample to see the global distribution
    search_params = {
        'taxonKey': family_key,
        'limit': 1000,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true'
    }
    
    search_resp = requests.get(search_url, params=search_params)
    search_resp.raise_for_status()
    sightings = search_resp.json()
    
    print(f"Found {len(sightings['results'])} sightings.")
    
    # Convert to DataFrame
    data = []
    for r in sightings['results']:
        data.append({
            'lat': r['decimalLatitude'],
            'lon': r['decimalLongitude'],
            'species': r.get('species', 'Unknown Penguin')
        })
    df = pd.DataFrame(data)
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting penguin distribution...")
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#e0f2f1') # Light icy blue
    ax.set_facecolor('#e0f2f1')
    
    # Plot world map
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        world_resp = requests.get(world_url)
        world_data = world_resp.json()
        world = gpd.GeoDataFrame.from_features(world_data['features'])
        world.set_crs(epsg=4326, inplace=True)
        world.plot(ax=ax, color='#ffffff', edgecolor='#b2dfdb', linewidth=0.5)
    except:
        pass
    
    # Plot sightings
    gdf.plot(
        ax=ax, 
        column='species', 
        cmap='tab20', 
        markersize=15, 
        alpha=0.6,
        legend=True,
        legend_kwds={'title': "Penguin Species", 'loc': 'lower left', 'bbox_to_anchor': (0, 0.1), 'fontsize': 8}
    )
    
    # Focus on the Southern Hemisphere
    ax.set_ylim(-90, 10)
    
    ax.set_axis_off()
    ax.set_title("Day 5: Earth - Global Distribution of Penguins", fontsize=24, pad=20, fontweight='bold', color='#004d40')
    
    ax.text(0.5, 0.02, "Data: GBIF | Theme: Birds | Element: Earth", 
            transform=ax.transAxes, ha='center', color='#00695c', fontsize=10)
    
    output_path = os.path.join('2025', 'day_5', 'visualization', 'penguin_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#e0f2f1')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 5: Earth (Classical Elements 1/4)
A global distribution map of penguins (family *Spheniscidae*). Being flightless and terrestrial during breeding, penguins are uniquely tied to the earth and southern oceans. Data sourced from GBIF sightings.

## Visualization
![Penguin Distribution](visualization/penguin_distribution.png)
"""
    with open(os.path.join('2025', 'day_5', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
