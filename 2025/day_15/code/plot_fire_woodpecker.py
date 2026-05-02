import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
import osmnx as ox

def main():
    print("Finding Black-backed Woodpecker (Picoides arcticus) in GBIF...")
    bird_name = "Picoides arcticus"
    match_url = "https://api.gbif.org/v1/species/match"
    match_params = {'name': bird_name, 'kingdom': 'Animalia'}
    
    match_resp = requests.get(match_url, params=match_params)
    match_resp.raise_for_status()
    bird_key = match_resp.json()['usageKey']
    
    print(f"Fetching sightings for {bird_name} (Key: {bird_key}) in California...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    # Filter for California (US-CA)
    search_params = {
        'taxonKey': bird_key,
        'limit': 500,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true',
        'country': 'US',
        'stateProvince': 'California'
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
            'species': r.get('species', bird_name)
        })
    df = pd.DataFrame(data)
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting fire-specialist bird distribution...")
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    # Plot California boundary
    state = ox.geocode_to_gdf("California, USA")
    state.plot(ax=ax, color='#2c2c2c', edgecolor='#444444', linewidth=1)
    
    # Plot sightings as "embers" (Orange/Fire colors)
    gdf.plot(
        ax=ax, 
        color='#f97316', # Bright orange like fire embers
        markersize=20, 
        alpha=0.6, 
        edgecolor='#fb923c', 
        linewidth=0.2,
        label='Woodpecker Sighting'
    )
    
    ax.set_axis_off()
    ax.set_title("Day 15: Fire - Black-backed Woodpecker in CA", color='#f97316', fontsize=22, pad=20, fontweight='bold')
    
    ax.text(0.5, 0.02, "Data: GBIF | Theme: Birds | Element: Fire", 
            transform=ax.transAxes, ha='center', color='#78716c', fontsize=10)
    
    output_path = os.path.join('2025', 'day_15', 'visualization', 'fire_woodpecker_dist.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 15: Fire (Classical Elements 3/4)
A distribution map of the **Black-backed Woodpecker** (*Picoides arcticus*) in California. This species is a fire specialist, heavily dependent on recently burned forests where it feeds on wood-boring beetle larvae. This visualization highlights the ecological relationship between wildfire and specialized avian biodiversity.

## Visualization
![Fire Woodpecker Distribution](visualization/fire_woodpecker_dist.png)
"""
    with open(os.path.join('2025', 'day_15', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
