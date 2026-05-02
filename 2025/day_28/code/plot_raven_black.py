import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
import osmnx as ox

def main():
    print("Finding Common Raven (Corvus corax) in GBIF...")
    bird_name = "Corvus corax"
    match_url = "https://api.gbif.org/v1/species/match"
    match_resp = requests.get(match_url, params={'name': bird_name})
    bird_key = match_resp.json()['usageKey']
    
    print(f"Fetching sightings for {bird_name} in SF...")
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': bird_key,
        'limit': 500,
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
    }
    
    search_resp = requests.get(search_url, params=search_params)
    data = []
    for r in search_resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting the black map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    # Extreme black theme
    fig.patch.set_facecolor('#000000')
    ax.set_facecolor('#000000')
    
    # Plot SF boundary in very dark gray
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    city.plot(ax=ax, color='#080808', edgecolor='#1a1a1a', linewidth=1)
    
    # Plot Raven sightings with a sharper, glowing dark aesthetic
    # Outer glow (deep purple/charcoal)
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='#1f1f2e', s=250, alpha=0.4, edgecolor='none')
    # Inner point (black with a sharp border)
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='black', s=40, alpha=0.9, edgecolor='#3b3b4f', linewidth=1.5)
    
    # Focus tightly on the SF Peninsula, ignoring the Farallon Islands
    ax.set_xlim(-122.52, -122.35)
    ax.set_ylim(37.70, 37.82)
    
    ax.set_axis_off()
    ax.set_title("Day 28: Black - Shadows of the Raven in SF", color='#262626', fontsize=22, pad=20, fontweight='black')
    
    output_path = os.path.join('2025', 'day_28', 'visualization', 'raven_black_map.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#000000')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 28: Black
A radical, low-contrast "black-on-black" map of **Common Raven** (*Corvus corax*) sightings in San Francisco. This visualization captures the mysterious and shadowy essence of the raven, using a dark charcoal palette that challenges the viewer to look closer at the urban landscape.

## Visualization
![Raven Black Map](visualization/raven_black_map.png)
"""
    with open(os.path.join('2025', 'day_28', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
