import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
import osmnx as ox

def main():
    print("Redoing Day 1 with a total makeover...")
    location = "San Francisco, California, USA"
    
    # 1. Fetch Water and Parks for richness
    print("Fetching base layers...")
    water = ox.features_from_place(location, tags={'natural': 'water', 'bay': True})
    parks = ox.features_from_place(location, tags={'leisure': 'park'})
    
    # 2. Fetch Anna's Hummingbird sightings
    print("Fetching Hummingbird sightings...")
    bird_name = "Calypte anna"
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 2476674, # Key from Day 1
        'limit': 500,
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-122.52 37.70, -122.35 37.70, -122.35 37.82, -122.52 37.82, -122.52 37.70))'
    }
    resp = requests.get(search_url, params=search_params)
    data = []
    for r in resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    gdf = gpd.GeoDataFrame(pd.DataFrame(data), geometry=gpd.points_from_xy([d['lon'] for d in data], [d['lat'] for d in data]), crs="EPSG:4326")
    
    print("Plotting Masterpiece Makeover...")
    fig, ax = plt.subplots(figsize=(15, 15))
    fig.patch.set_facecolor('#0f172a') # Elegant deep navy
    ax.set_facecolor('#0f172a')
    
    # Plot Water
    water.plot(ax=ax, color='#1e3a8a', alpha=0.6, zorder=0)
    
    # Plot SF Boundary
    city = ox.geocode_to_gdf(location)
    city.plot(ax=ax, color='#1e293b', edgecolor='#334155', linewidth=2, zorder=1)
    
    # Plot Parks
    parks.plot(ax=ax, color='#065f46', alpha=0.4, zorder=2)
    
    # Plot Hummingbird sightings with a "ruby glow"
    # Outer glow
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='#f43f5e', s=50, alpha=0.2, zorder=10)
    # Inner point
    ax.scatter(gdf.geometry.x, gdf.geometry.y, color='#f43f5e', s=10, alpha=0.8, edgecolor='white', linewidth=0.2, zorder=11)
    
    # Add high-level labels for hotspots
    hotspots = [
        ('Golden Gate Park', -122.48, 37.77),
        ('The Presidio', -122.46, 37.80),
        ('Glen Canyon', -122.44, 37.74),
        ('Bernal Heights', -122.41, 37.74)
    ]
    for name, lon, lat in hotspots:
        ax.text(lon, lat, name, color='#94a3b8', fontsize=12, fontweight='bold', ha='center', zorder=15)
        
    ax.set_axis_off()
    ax.set_title("San Francisco: Portrait of the Anna's Hummingbird", color='white', fontsize=32, pad=30, fontweight='black')
    
    ax.text(0.5, 0.01, "#30DayMapChallenge 2025 - Theme: Birds | Makeover Finale", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=14)
    
    output_path = os.path.join('2025', 'day_30', 'visualization', 'sf_hummingbird_makeover.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f172a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 30: Makeover
The grand finale of the 2025 Birds-themed challenge. This is a comprehensive makeover of the Day 1 map, presenting a polished portrait of **Anna's Hummingbird** sightings in San Francisco. The map layers refined city boundaries, lush green parks, and deep blue water to create a definitive celebration of urban avian life.

## Visualization
![SF Hummingbird Makeover](visualization/sf_hummingbird_makeover.png)
"""
    with open(os.path.join('2025', 'day_30', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
