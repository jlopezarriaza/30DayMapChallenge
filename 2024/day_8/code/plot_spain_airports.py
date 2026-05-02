import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
from io import StringIO

def main():
    print("Fetching Spain airports data from HDX...")
    url = "https://data.humdata.org/dataset/63017d9e-f0e2-4e08-a3b6-050384d05490/resource/8ba09b5b-e23f-485b-acb6-e232b4e3a26b/download/airports-in-spain.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print(f"Found {len(df)} airports.")
    
    # Filter for interesting ones (exclude closed)
    df = df[df['type'] != 'closed']
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.longitude_deg, df.latitude_deg),
        crs="EPSG:4326"
    )
    
    # Fetch Spain boundary for context
    print("Fetching Spain boundary...")
    boundary_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/ESP.geo.json"
    try:
        resp = requests.get(boundary_url)
        resp.raise_for_status()
        data = resp.json()
        world = gpd.GeoDataFrame.from_features(data['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error fetching boundary: {e}")
        return
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#eef2f3')
    ax.set_facecolor('#eef2f3')
    
    # Plot country boundary
    world.plot(ax=ax, color='#d1d8e0', edgecolor='#4b6584', linewidth=0.5)
    
    # Plot airports by type
    # small_airport, medium_airport, large_airport, heliport, etc.
    airport_types = gdf['type'].unique()
    colors = {'large_airport': '#eb3b5a', 'medium_airport': '#fa8231', 'small_airport': '#f7b731', 'heliport': '#20bf6b'}
    
    for atype in airport_types:
        if atype in colors:
            gdf[gdf['type'] == atype].plot(
                ax=ax, 
                color=colors[atype], 
                label=atype.replace('_', ' ').title(),
                markersize=20 if atype == 'large_airport' else 10,
                alpha=0.7
            )
    
    ax.set_axis_off()
    ax.set_title('Airports and Heliports in Spain (HDX Data)', fontsize=20, pad=20, fontweight='bold')
    ax.legend(loc='lower left', frameon=True, facecolor='white', title="Airport Type")
    
    output_path = os.path.join('2024', 'day_8', 'visualization', 'spain_airports.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#eef2f3')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
