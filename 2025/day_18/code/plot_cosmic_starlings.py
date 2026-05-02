import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Finding Common Starling (Sturnus vulgaris) in GBIF...")
    bird_name = "Sturnus vulgaris"
    match_url = "https://api.gbif.org/v1/species/match"
    match_resp = requests.get(match_url, params={'name': bird_name})
    bird_key = match_resp.json()['usageKey']
    
    print(f"Fetching sightings for {bird_name} in North America...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': bird_key,
        'limit': 1000,
        'basisOfRecord': 'HUMAN_OBSERVATION',
        'hasCoordinate': 'true',
        'country': 'US'
    }
    
    search_resp = requests.get(search_url, params=search_params)
    data = []
    for r in search_resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting cosmic map...")
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#020617') # Space black
    ax.set_facecolor('#020617')
    
    # Plot US boundary (subtle)
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        world_resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(world_resp.json()['features'])
        usa = world[world['name'] == 'United States of America']
        usa.plot(ax=ax, color='#1e293b', edgecolor='#334155', linewidth=0.5, alpha=0.3)
    except:
        pass
    
    # Plot sightings as "stars"
    # Use a glowing effect with multiple scatter calls
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='#818cf8', s=20, alpha=0.1) # Outer glow
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='#c084fc', s=10, alpha=0.3) # Inner glow
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='white', s=2, alpha=0.8) # Star center
    
    ax.set_axis_off()
    ax.set_title("Day 18: Out of This World - The Starling Nebula", color='white', fontsize=26, pad=20, fontweight='black', fontname='monospace')
    
    ax.text(0.5, 0.05, "Mapping Sturnus vulgaris sightings as a celestial cluster | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#94a3b8', fontsize=12, fontname='monospace')
    
    output_path = os.path.join('2025', 'day_18', 'visualization', 'starling_nebula.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#020617')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 18: Out of this world
A "cosmic" visualization of **Common Starling** (*Sturnus vulgaris*) sightings across the United States. Playing on their name, the sightings are plotted with a glowing, star-like aesthetic against a deep space background, imagining the distribution as a galactic nebula.

## Visualization
![Starling Nebula](visualization/starling_nebula.png)
"""
    with open(os.path.join('2025', 'day_18', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
