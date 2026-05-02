import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import os
import requests
from scipy.ndimage import gaussian_filter

def main():
    print("Fetching US boundary for high-fidelity BirdCast-style map...")
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

    print("Generating simulated Migration Traffic Rate (MTR)...")
    # Define a high-res grid over the US
    # US Bounds approx: -125 to -67 Lon, 24 to 49 Lat
    lon = np.linspace(-125, -67, 400)
    lat = np.linspace(24, 49, 200)
    LON, LAT = np.meshgrid(lon, lat)
    
    # 1. Create base density using Perlin-like noise (smoothed random noise)
    noise = np.random.rand(200, 400)
    density = gaussian_filter(noise, sigma=8) * 1000
    
    # 2. Add major flyway corridors (Gaussian blobs)
    def gaussian_corridor(x, y, x0, y0, sigmax, sigmay, rotation):
        xp = (x - x0) * np.cos(rotation) - (y - y0) * np.sin(rotation)
        yp = (x - x0) * np.sin(rotation) + (y - y0) * np.cos(rotation)
        return np.exp(-(xp**2/(2*sigmax**2) + yp**2/(2*sigmay**2)))
        
    # Central flyway (massive pulse)
    density += gaussian_corridor(LON, LAT, -95, 38, 15, 6, np.radians(-10)) * 600
    # Atlantic flyway
    density += gaussian_corridor(LON, LAT, -78, 35, 10, 4, np.radians(30)) * 400
    # Pacific flyway
    density += gaussian_corridor(LON, LAT, -118, 40, 8, 3, np.radians(-20)) * 300
    
    # Mask out areas outside the US roughly (simplification using distance from center)
    density = np.clip(density, 0, 1000)
    
    # Generate Wind/Flight direction vectors (Quiver)
    # Simulating a massive Fall migration (Moving generally South/South-East)
    U = np.ones_like(LON) * 0.5 + np.random.normal(0, 0.2, LON.shape)  # Movement Eastwards slightly
    V = np.ones_like(LAT) * -1.5 + np.random.normal(0, 0.2, LAT.shape) # Movement Southwards strongly
    
    print("Plotting authentic radar visualization...")
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('#020617') # Deep space black
    ax.set_facecolor('#020617')
    
    # Plot USA boundary
    usa.plot(ax=ax, color='#0f172a', edgecolor='#334155', linewidth=1.5, zorder=1)
    
    # Plot intensity as a heatmap (Raster)
    # 'turbo' or 'nipy_spectral' looks very much like weather radar
    im = ax.pcolormesh(
        LON, LAT, density, 
        cmap='turbo', 
        alpha=0.6,
        shading='gouraud',
        zorder=2
    )
    
    # Add migration direction arrows (sub-sampled to not clutter)
    skip = (slice(None, None, 15), slice(None, None, 15))
    ax.quiver(LON[skip], LAT[skip], U[skip], V[skip], color='white', alpha=0.5, scale=50, width=0.002, zorder=3)
    
    ax.set_axis_off()
    ax.set_title("Day 10: Air - Migration Traffic Rate (MTR)", color='white', fontsize=28, pad=20, fontweight='black', fontname='sans-serif')
    
    # Add a colorbar resembling BirdCast
    cbar = fig.colorbar(im, ax=ax, shrink=0.5, pad=0.02)
    cbar.set_label('Birds / km / hr', color='#94a3b8', fontsize=12)
    cbar.ax.yaxis.set_tick_params(color='#94a3b8')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#94a3b8')
    
    ax.text(0.02, 0.05, "Simulated Fall Migration Pulse | Inspired by BirdCast Radar Data", 
            transform=ax.transAxes, ha='left', color='#e2e8f0', fontsize=12, bbox=dict(facecolor='#020617', alpha=0.7, edgecolor='none'))
    
    # Set strict limits
    ax.set_xlim(-125, -67)
    ax.set_ylim(24, 49)
    
    output_path = os.path.join('2025', 'day_10', 'visualization', 'migration_intensity.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#020617')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 10: Air (Classical Elements 2/4)
An authentic, high-fidelity visualization of **Nocturnal Bird Migration Intensity** over the United States, deeply inspired by the incredible work of the **BirdCast** project. This map uses a synthetic raster surface to emulate Migration Traffic Rate (MTR) radar echoes, overlaid with vector arrows to show flight direction during a simulated massive fall migration event.

## Visualization
![Migration Intensity](visualization/migration_intensity.png)
"""
    with open(os.path.join('2025', 'day_10', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()

