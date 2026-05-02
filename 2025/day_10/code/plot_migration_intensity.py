import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import os
import requests

def main():
    print("Fetching US boundary for migration map...")
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        resp = requests.get(world_url)
        data = resp.json()
        world = gpd.GeoDataFrame.from_features(data['features'])
        world.set_crs(epsg=4326, inplace=True)
        usa = world[world['name'] == 'United States of America']
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Generating simulated migration intensity (BirdCast style)...")
    # Define a grid over the US
    # US Bounds approx: -125 to -67 Lon, 24 to 49 Lat
    lon = np.linspace(-125, -67, 200)
    lat = np.linspace(24, 49, 100)
    LON, LAT = np.meshgrid(lon, lat)
    
    # Create some "migration pulses" (Gaussian blobs)
    def gaussian(x, y, x0, y0, sigmax, sigmay):
        return np.exp(-((x-x0)**2/(2*sigmax**2) + (y-y0)**2/(2*sigmay**2)))
        
    intensity = (
        gaussian(LON, LAT, -95, 35, 10, 5) * 100 +  # Central flyway pulse
        gaussian(LON, LAT, -80, 40, 5, 8) * 80 +    # Atlantic flyway pulse
        gaussian(LON, LAT, -120, 38, 4, 6) * 60     # Pacific flyway pulse
    )
    # Add some noise
    intensity += np.random.normal(0, 5, intensity.shape)
    intensity = np.clip(intensity, 0, 100)
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#020617') # Near black
    ax.set_facecolor('#020617')
    
    # Plot USA boundary
    usa.plot(ax=ax, color='none', edgecolor='#1e293b', linewidth=2)
    
    # Plot intensity as a heatmap
    im = ax.imshow(
        intensity, 
        extent=[-125, -67, 24, 49], 
        origin='lower', 
        cmap='magma', # BirdCast often uses similar warm-on-dark palettes
        alpha=0.8,
        interpolation='bilinear'
    )
    
    ax.set_axis_off()
    ax.set_title("Day 10: Air - Nocturnal Bird Migration Intensity", color='white', fontsize=26, pad=20, fontweight='black')
    
    # Add a colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.5, label='Birds per km² (Simulated)')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    ax.text(0.5, 0.05, "Inspired by BirdCast | Element: Air | Theme: Birds", 
            transform=ax.transAxes, ha='center', color='#94a3b8', fontsize=12)
    
    output_path = os.path.join('2025', 'day_10', 'visualization', 'migration_intensity.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#020617')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 10: Air (Classical Elements 2/4)
A continental-scale heatmap of simulated **Nocturnal Bird Migration Intensity** over the United States. Inspired by BirdCast, this map visualizes the massive pulses of birds taking to the air during peak migration nights.

## Visualization
![Migration Intensity](visualization/migration_intensity.png)
"""
    with open(os.path.join('2025', 'day_10', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
