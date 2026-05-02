import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Finding Black-footed Albatross (Phoebastria nigripes) in GBIF...")
    bird_name = "Phoebastria nigripes"
    match_url = "https://api.gbif.org/v1/species/match"
    match_resp = requests.get(match_url, params={'name': bird_name})
    bird_key = match_resp.json()['usageKey']
    
    print(f"Fetching sightings for {bird_name} in the North Pacific...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    # Large area query for North Pacific
    search_params = {
        'taxonKey': bird_key,
        'limit': 1000,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((120 20, -110 20, -110 65, 120 65, 120 20))' # North Pacific
    }
    
    search_resp = requests.get(search_url, params=search_params)
    data = []
    for r in search_resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting oceanic distribution...")
    fig, ax = plt.subplots(figsize=(15, 10))
    # Deep oceanic blue background
    fig.patch.set_facecolor('#1e3a8a')
    ax.set_facecolor('#1e3a8a')
    
    # Plot world map for land context (dark and subtle)
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        world_resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(world_resp.json()['features'])
        world.plot(ax=ax, color='#0f172a', edgecolor='#334155', linewidth=0.5)
    except:
        pass
    
    # Plot albatross sightings as water-colored points
    gdf.plot(
        ax=ax, 
        color='#60a5fa', # Brighter blue points
        markersize=10, 
        alpha=0.5, 
        edgecolor='#93c5fd', 
        linewidth=0.2,
        label='Albatross Sighting'
    )
    
    # Focus on the North Pacific
    ax.set_xlim(120, -110) # Wrap-around issues might occur here, let's keep it simple
    # Adjust for Pacific centered view if needed, but standard Lon is -180 to 180
    ax.set_xlim(-180, 180) # Reset to full view for safety
    ax.set_ylim(10, 70)
    
    ax.set_axis_off()
    ax.set_title("Day 20: Water - Black-footed Albatross Range", color='#60a5fa', fontsize=26, pad=20, fontweight='black')
    
    ax.text(0.5, 0.05, "Mapping pelagic sightings across the Pacific | Theme: Birds | Element: Water", 
            transform=ax.transAxes, ha='center', color='#93c5fd', fontsize=12)
    
    output_path = os.path.join('2025', 'day_20', 'visualization', 'pelagic_albatross_dist.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1e3a8a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 20: Water (Classical Elements 4/4)
A distribution map of the **Black-footed Albatross** (*Phoebastria nigripes*) across the North Pacific Ocean. These pelagic birds live almost entirely on the open water, returning to land only for breeding. This visualization celebrates the fourth classical element through the range of an ocean-bound species.

## Visualization
![Pelagic Albatross Distribution](visualization/pelagic_albatross_dist.png)
"""
    with open(os.path.join('2025', 'day_20', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
