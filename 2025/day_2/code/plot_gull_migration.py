import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from shapely.geometry import LineString

import requests
from io import StringIO

def main():
    print("Fetching Lesser Black-backed Gull tracking data...")
    url = "https://raw.githubusercontent.com/gabrieldluca/bird-migration/master/bird_tracking.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print(f"Found {len(df)} tracking points for birds: {df['bird_name'].unique()}")
    
    # Filter for a specific bird or just group by bird
    # Birds: Eric, Nico, Sanne
    
    print("Creating trajectories...")
    bird_lines = []
    for bird in df['bird_name'].unique():
        bird_df = df[df['bird_name'] == bird].sort_values('date_time')
        if len(bird_df) > 1:
            line = LineString(zip(bird_df.longitude, bird_df.latitude))
            bird_lines.append({'bird_name': bird, 'geometry': line})
            
    gdf = gpd.GeoDataFrame(bird_lines, crs="EPSG:4326")
    
    print("Plotting migration lines...")
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')
    
    # Plot world map for context
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        resp.raise_for_status()
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error fetching world map: {e}")
        return
    world.plot(ax=ax, color='#e2e8f0', edgecolor='#cbd5e1', linewidth=0.5)
    
    # Plot bird trajectories
    colors = {'Eric': '#2563eb', 'Nico': '#d97706', 'Sanne': '#059669'}
    for bird in gdf['bird_name'].unique():
        gdf[gdf['bird_name'] == bird].plot(
            ax=ax, 
            color=colors.get(bird, 'black'), 
            linewidth=2, 
            alpha=0.8, 
            label=bird
        )
    
    # Focus on the area of interest (Europe/Africa)
    ax.set_xlim(-20, 20)
    ax.set_ylim(10, 60)
    
    ax.set_axis_off()
    ax.set_title("Day 2: Lines - Lesser Black-backed Gull Migration", fontsize=24, pad=20, fontweight='bold')
    ax.legend(title="Bird ID", loc='lower left')
    
    output_path = os.path.join('2025', 'day_2', 'visualization', 'gull_migration_lines.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 2: Lines
A map visualizing the migratory trajectories of three Lesser Black-backed Gulls (Eric, Nico, and Sanne), tracked via GPS. Data provided by the LifeWatch INBO bird tracking network.

## Visualization
![Gull Migration Lines](visualization/gull_migration_lines.png)
"""
    with open(os.path.join('2025', 'day_2', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
