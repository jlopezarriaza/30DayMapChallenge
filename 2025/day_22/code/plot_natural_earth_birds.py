import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests
from io import StringIO

def main():
    print("Fetching endemic bird species data...")
    url_data = "https://ourworldindata.org/grapher/endemic-bird-species-by-country.csv?v=1&csvType=full&useColumnShortNames=false"
    try:
        resp = requests.get(url_data)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text))
        # Keep only the latest year for each country
        df = df.sort_values('Year').drop_duplicates('Entity', keep='last')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print("Fetching Natural Earth world map...")
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        world = gpd.GeoDataFrame.from_features(resp.json()['features'])
        world.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Joining data...")
    # Join on country name (Entity in CSV, name in GeoJSON)
    # Some names might not match exactly, but let's try a simple join first
    world = world.merge(df, left_on='name', right_on='Entity', how='left')
    
    # Fill NaN counts with 0
    # The column name in the CSV for count is usually 'Endemic bird species (BirdLife International (2021))' or similar
    # Let's find the column that isn't Entity, Code, or Year
    count_col = [c for c in df.columns if c not in ['Entity', 'Code', 'Year']][0]
    world[count_col] = world[count_col].fillna(0)

    print("Plotting...")
    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor('#ffffff')
    
    # Use Robinson projection
    world_robinson = world.to_crs('+proj=robin')
    
    world_robinson.plot(
        ax=ax, 
        column=count_col, 
        cmap='YlGnBu', 
        edgecolor='black', 
        linewidth=0.2,
        legend=True,
        legend_kwds={'label': "Number of Endemic Bird Species", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    ax.set_axis_off()
    ax.set_title("Day 22: Natural Earth - Global Bird Endemism", fontsize=24, pad=20, fontweight='bold')
    
    ax.text(0.5, 0.02, "Data: Our World in Data / BirdLife International | Theme: Birds | Data: Natural Earth", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=10)
    
    output_path = os.path.join('2025', 'day_22', 'visualization', 'global_bird_endemism.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 22: Data challenge: Natural Earth
A global choropleth map visualizing the richness of endemic bird species by country. Using Natural Earth boundaries and data from BirdLife International (via Our World in Data), this map highlights countries with unique avian biodiversity found nowhere else on Earth.

## Visualization
![Global Bird Endemism](visualization/global_bird_endemism.png)
"""
    with open(os.path.join('2025', 'day_22', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
