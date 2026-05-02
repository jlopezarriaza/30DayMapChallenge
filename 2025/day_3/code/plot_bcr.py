import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Fetching Important Bird Areas (IBAs) of California...")
    # Audubon REST API for IBAs in California
    url = "https://gis.audubon.org/arcgisweb/rest/services/NAS/ImportantBirdAreas_Polygon/MapServer/0/query?where=STATE%3D'California'&outFields=*&f=geojson"
    
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        gdf = gpd.GeoDataFrame.from_features(data['features'])
        gdf.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error fetching IBA data: {e}")
        return

    print(f"Found {len(gdf)} Important Bird Areas.")
    
    print("Plotting IBA polygons...")
    fig, ax = plt.subplots(figsize=(12, 15))
    fig.patch.set_facecolor('#fdfdfd')
    ax.set_facecolor('#fdfdfd')
    
    # Plot IBAs with a nice earthy colormap
    gdf.plot(
        ax=ax, 
        column='SITE_NAME', 
        cmap='viridis', 
        edgecolor='#276749', 
        linewidth=0.2,
        alpha=0.7
    )
    
    # Plot California boundary for context
    import osmnx as ox
    state = ox.geocode_to_gdf("California, USA")
    state.plot(ax=ax, color='none', edgecolor='#cbd5e1', linewidth=1, zorder=0)
    
    ax.set_axis_off()
    ax.set_title("Day 3: Polygons - CA Important Bird Areas", fontsize=24, pad=20, fontweight='bold', color='#1a365d')
    
    ax.text(0.5, 0.02, "Data: National Audubon Society | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#64748b', fontsize=10)
    
    output_path = os.path.join('2025', 'day_3', 'visualization', 'ca_important_bird_areas.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 3: Polygons
A map of the **Important Bird Areas (IBAs)** in California. IBAs are sites that provide essential habitat for one or more species of breeding, wintering, or migrating birds. Data provided by the National Audubon Society.

## Visualization
![California Important Bird Areas](visualization/ca_important_bird_areas.png)
"""
    with open(os.path.join('2025', 'day_3', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
