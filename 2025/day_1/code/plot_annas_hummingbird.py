import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import osmnx as ox
import requests

def main():
    print("Finding Anna's Hummingbird (Calypte anna) in GBIF...")
    bird_name = "Calypte anna"
    match_url = "https://api.gbif.org/v1/species/match"
    match_params = {'name': bird_name, 'kingdom': 'Animalia'}
    
    match_resp = requests.get(match_url, params=match_params)
    match_resp.raise_for_status()
    bird_key = match_resp.json()['usageKey']
    
    print(f"Fetching sightings for {bird_name} (Key: {bird_key}) in SF...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': bird_key,
        'limit': 300,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
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
            'date': r.get('eventDate', 'Unknown'),
            'species': r.get('species', bird_name)
        })
    df = pd.DataFrame(data)
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0f172a') # Deep navy
    ax.set_facecolor('#0f172a')
    
    # Plot SF boundary
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    city.plot(ax=ax, color='#1e293b', edgecolor='#334155', linewidth=1)
    
    # Plot sightings as "ruby" points
    gdf.plot(
        ax=ax, 
        color='#f43f5e', # Ruby/Pinkish red
        markersize=25, 
        alpha=0.7, 
        edgecolor='white', 
        linewidth=0.5
    )
    
    ax.set_axis_off()
    ax.set_title("Day 1: Points - Anna's Hummingbird in SF", color='white', fontsize=22, pad=20, fontweight='bold')
    ax.text(0.5, 0.02, "Data: GBIF (Human Observations) | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#94a3b8', fontsize=10)
    
    output_path = os.path.join('2025', 'day_1', 'visualization', 'annas_hummingbird_points.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f172a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 1: Points
A point map showing recent human observations of **Anna's Hummingbird** (*Calypte anna*) in San Francisco, sourced from the Global Biodiversity Information Facility (GBIF).

## Visualization
![Anna's Hummingbird Points](visualization/annas_hummingbird_points.png)
"""
    with open(os.path.join('2025', 'day_1', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
