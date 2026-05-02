import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.ndimage import gaussian_filter

def main():
    print("Generating synthetic 'process' data...")
    # 1. Raw Data: 200 points in SF + 20 outliers in the ocean/mountains
    sf_center = [-122.44, 37.76]
    raw_points = np.random.normal(sf_center, 0.03, (200, 2))
    outliers = np.random.normal([-122.1, 37.5], 0.1, (20, 2))
    all_points = np.vstack([raw_points, outliers])
    
    raw_df = pd.DataFrame(all_points, columns=['lon', 'lat'])
    raw_gdf = gpd.GeoDataFrame(raw_df, geometry=gpd.points_from_xy(raw_df.lon, raw_df.lat), crs="EPSG:4326")
    
    print("Cleaning data...")
    # 2. Filtered Data: Clip to SF bounds
    import osmnx as ox
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    clean_gdf = gpd.clip(raw_gdf, city)
    
    print("Analyzing data...")
    # 3. Density Data: Create a raster surface from clean points
    heatmap, xedges, yedges = np.histogram2d(clean_gdf.geometry.x, clean_gdf.geometry.y, bins=50)
    heatmap = gaussian_filter(heatmap, sigma=1)
    
    print("Plotting process panels...")
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8))
    fig.patch.set_facecolor('#f8fafc')
    
    # Panel 1: Raw
    ax1.scatter(all_points[:, 0], all_points[:, 1], color='#ef4444', s=10, alpha=0.5)
    ax1.set_title("1. Raw Data (w/ Outliers)", fontsize=16, fontweight='bold')
    ax1.set_axis_off()
    
    # Panel 2: Cleaned
    city.plot(ax=ax2, color='#f1f5f9', edgecolor='#cbd5e1')
    clean_gdf.plot(ax=ax2, color='#2563eb', markersize=10, alpha=0.6)
    ax2.set_title("2. Cleaned & Clipped", fontsize=16, fontweight='bold')
    ax2.set_axis_off()
    
    # Panel 3: Analyzed
    city.plot(ax=ax3, color='#0f172a', edgecolor='#334155')
    ax3.imshow(heatmap.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], 
               origin='lower', cmap='YlOrRd', alpha=0.8, interpolation='bilinear')
    ax3.set_title("3. Analyzed Density", fontsize=16, fontweight='bold')
    ax3.set_axis_off()
    
    plt.suptitle("Day 23: Process - The Avian Mapping Pipeline", fontsize=24, y=1.05, fontweight='black')
    plt.tight_layout()
    
    output_path = os.path.join('2025', 'day_23', 'visualization', 'mapping_process.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 23: Process
A meta-map visualizing the "process" of turning raw biodiversity sightings into an analyzed density surface. The three panels show: 1) Raw input data with spatial outliers, 2) Cleaned data clipped to a study area, and 3) A final density visualization using Kernel Density Estimation.

## Visualization
![Mapping Process](visualization/mapping_process.png)
"""
    with open(os.path.join('2025', 'day_23', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
