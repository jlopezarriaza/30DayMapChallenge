import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def main():
    print("Fetching SF neighborhoods for typography map...")
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/san-francisco.geojson"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        gdf = gpd.GeoDataFrame.from_features(data['features'])
        gdf.set_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Plotting typography map...")
    fig, ax = plt.subplots(figsize=(15, 15))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Calculate centroids for label placement
    gdf['centroid'] = gdf.geometry.centroid
    
    # Scale font size by neighborhood area (rough proxy for importance/size)
    # Area in degrees is small, but relative size matters
    gdf['area'] = gdf.geometry.area
    min_area = gdf['area'].min()
    max_area = gdf['area'].max()
    
    for idx, row in gdf.iterrows():
        name = row['name']
        x, y = row['centroid'].x, row['centroid'].y
        
        # Scale font size between 8 and 20
        # normalize area
        if max_area > min_area:
            size = 8 + 12 * (row['area'] - min_area) / (max_area - min_area)
        else:
            size = 12
            
        ax.text(x, y, name, 
                fontsize=size, 
                ha='center', 
                va='center', 
                fontweight='bold', 
                fontfamily='serif',
                alpha=0.8,
                rotation=10 if size > 15 else 0 # Slight tilt for big ones
        )
    
    # Plot a very subtle outline of SF for context
    gdf.boundary.plot(ax=ax, color='#eeeeee', linewidth=0.5, alpha=0.5)
    
    ax.set_axis_off()
    ax.set_title('The Names of San Francisco', fontsize=28, pad=20, fontfamily='serif', fontweight='black')
    
    output_path = os.path.join('2024', 'day_19', 'visualization', 'sf_typography.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
