import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import os
from scipy.ndimage import gaussian_filter

def main():
    print("Fetching bird sightings for raster surface...")
    # Regional query for SF Bay Area
    search_url = "https://api.gbif.org/v1/occurrence/search"
    search_params = {
        'taxonKey': 212,
        'limit': 1000,
        'hasCoordinate': 'true',
        'geometry': 'POLYGON((-123.0 37.3, -121.5 37.3, -121.5 38.3, -123.0 38.3, -123.0 37.3))'
    }
    
    resp = requests.get(search_url, params=search_params)
    data = []
    for r in resp.json()['results']:
        data.append({'lat': r['decimalLatitude'], 'lon': r['decimalLongitude']})
    df = pd.DataFrame(data)
    
    print("Generating raster surface...")
    x = df['lon'].values
    y = df['lat'].values
    
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=200)
    heatmap = gaussian_filter(heatmap, sigma=2)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    im = ax.imshow(
        heatmap.T, 
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], 
        origin='lower', 
        cmap='Greens', 
        alpha=0.9,
        interpolation='bilinear'
    )
    
    ax.set_axis_off()
    ax.set_title("Day 29: Raster - Avian Richness in the Bay Area", color='white', fontsize=24, pad=20, fontweight='bold')
    
    cbar = fig.colorbar(im, ax=ax, shrink=0.5, label='Sighting Intensity')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    output_path = os.path.join('2025', 'day_29', 'visualization', 'bay_area_bird_raster.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f172a')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 29: Raster
A continuous intensity surface (raster) of bird sightings across the San Francisco Bay Area. This map uses Gaussian smoothing on binned point data from GBIF to visualize regional "hotspots" of avian activity as a continuous field of biodiversity.

## Visualization
![Bay Area Bird Raster](visualization/bay_area_bird_raster.png)
"""
    with open(os.path.join('2025', 'day_29', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
