import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import osmnx as ox

def main():
    # Simulate "My Birding Data"
    # Sightings from 2024 in San Francisco
    my_data = [
        {'species': "Anna's Hummingbird", 'lat': 37.769, 'lon': -122.447, 'count': 3, 'date': '2024-03-12', 'location': 'Golden Gate Park'},
        {'species': "Great Blue Heron", 'lat': 37.808, 'lon': -122.475, 'count': 1, 'date': '2024-04-05', 'location': 'The Presidio'},
        {'species': "Peregrine Falcon", 'lat': 37.795, 'lon': -122.393, 'count': 2, 'date': '2024-05-20', 'location': 'Ferry Building'},
        {'species': "California Quail", 'lat': 37.783, 'lon': -122.502, 'count': 5, 'date': '2024-06-15', 'location': 'Land\'s End'},
        {'species': "Osprey", 'lat': 37.802, 'lon': -122.406, 'count': 1, 'date': '2024-07-02', 'location': 'Coit Tower'},
        {'species': "Western Bluebird", 'lat': 37.754, 'lon': -122.447, 'count': 4, 'date': '2024-08-18', 'location': 'Twin Peaks'},
        {'species': "Snowy Plover", 'lat': 37.771, 'lon': -122.511, 'count': 12, 'date': '2024-09-10', 'location': 'Ocean Beach'},
    ]
    
    df = pd.DataFrame(my_data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
    
    print("Plotting my birding data...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#fffcf0') # Warm cream
    ax.set_facecolor('#fffcf0')
    
    # Plot SF boundary
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    city.plot(ax=ax, color='#f5e6d3', edgecolor='#d4b483', alpha=0.5)
    
    # Plot my sightings
    # Use different markers or sizes? Let's just use color by species
    gdf.plot(
        ax=ax, 
        column='species', 
        cmap='Dark2', 
        markersize=150, 
        alpha=0.9, 
        edgecolor='black', 
        linewidth=1,
        legend=True,
        legend_kwds={'title': "Species Spotted", 'loc': 'lower left'}
    )
    
    # Add labels for locations
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.location):
        ax.text(x + 0.002, y + 0.002, label, fontsize=10, fontname='serif', fontweight='bold')
    
    ax.set_axis_off()
    ax.set_title("Day 4: My Data - SF Birding Lifelist 2024", fontsize=24, pad=20, fontname='serif', fontweight='bold', color='#4a3728')
    
    output_path = os.path.join('2025', 'day_4', 'visualization', 'my_birding_lifelist.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#fffcf0')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 4: Data challenge: My Data
A personalized visualization of a synthetic **Birding Lifelist** for 2024. This map plots various species sightings at key locations across San Francisco, representing a curated record of personal avian encounters.

## Visualization
![My Birding Lifelist](visualization/my_birding_lifelist.png)
"""
    with open(os.path.join('2025', 'day_4', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
