import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Finding House Sparrow (Passer domesticus) in GBIF...")
    bird_name = "Passer domesticus"
    match_url = "https://api.gbif.org/v1/species/match"
    match_resp = requests.get(match_url, params={'name': bird_name})
    bird_key = match_resp.json()['usageKey']
    
    print(f"Fetching global sightings for {bird_name}...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': bird_key,
        'limit': 1000,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true'
    }
    
    search_resp = requests.get(search_url, params=search_params)
    data = []
    for r in search_resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting global distribution...")
    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor('#fdfdfd')
    
    # Plot world map
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        world_resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(world_resp.json()['features'])
        world.plot(ax=ax, color='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.5)
    except:
        pass
    
    # Plot sparrow sightings as "cargo" points
    gdf.plot(
        ax=ax, 
        color='#92400e', # Brownish like a sparrow
        markersize=10, 
        alpha=0.4, 
        edgecolor='none',
        label='Sparrow Sighting'
    )
    
    ax.set_axis_off()
    ax.set_title("Day 26: Transport - The Global Reach of the House Sparrow", fontsize=24, pad=20, fontweight='bold', color='#451a03')
    
    ax.text(0.5, 0.05, "Mapping a species that spread globally via human transport networks | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#78350f', fontsize=12)
    
    output_path = os.path.join('2025', 'day_26', 'visualization', 'sparrow_transport.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 26: Transport
A global distribution map of the **House Sparrow** (*Passer domesticus*). This species is one of the most successful urban birds, having spread across the globe primarily by hitching rides on human transport infrastructure—from early wooden ships to modern rail and shipping networks.

## Visualization
![Sparrow Transport](visualization/sparrow_transport.png)
"""
    with open(os.path.join('2025', 'day_26', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
