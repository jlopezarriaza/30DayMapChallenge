import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import os
from scipy.ndimage import gaussian_filter

def get_sf_trees():
    """Fetch tree data from San Francisco's open data API."""
    api_endpoint = "https://data.sfgov.org/resource/tkzw-k3nq.json"
    api_params = {"$limit": 100000, "$offset": 0}
    response = requests.get(api_endpoint, params=api_params)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df = df.astype({"latitude": "float64", "longitude": "float64"})
    return df.dropna(subset=['latitude', 'longitude'])

def main():
    print("Fetching tree data...")
    df = get_sf_trees()
    
    # Define grid
    x = df['longitude'].values
    y = df['latitude'].values
    
    # Filter for SF bounds to avoid outliers
    mask = (x > -122.52) & (x < -122.35) & (y > 37.70) & (y < 37.82)
    x = x[mask]
    y = y[mask]
    
    print("Creating raster density...")
    # Create 2D histogram
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=500)
    
    # Smooth the heatmap to make it look like a continuous raster
    heatmap = gaussian_filter(heatmap, sigma=2)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('black')
    
    # Plot the raster
    # Note: transpose the heatmap for correct orientation
    im = ax.imshow(
        heatmap.T, 
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], 
        origin='lower', 
        cmap='YlGn',
        interpolation='bilinear'
    )
    
    ax.set_axis_off()
    ax.set_title('SF Urban Canopy Density (Raster)', color='white', fontsize=20, pad=20)
    
    # Add a colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.5, label='Tree Density')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    output_path = os.path.join('2024', 'day_6', 'visualization', 'sf_tree_raster.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
