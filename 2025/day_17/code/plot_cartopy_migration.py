import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os
import numpy as np
import ssl
import urllib

def main():
    print("Creating global migration map with Cartopy...")
    
    # Handle SSL verification issues for Cartopy downloads
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    fig = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.Robinson()})[1]
    fig.patch.set_facecolor('#fdfdfd')
    
    # Add features
    fig.add_feature(cfeature.LAND, facecolor='#f1f5f9')
    fig.add_feature(cfeature.OCEAN, facecolor='#e0f2fe')
    fig.add_feature(cfeature.COASTLINE, edgecolor='#94a3b8', linewidth=0.5)
    fig.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='#94a3b8')
    
    # Define a long migration path (e.g., Arctic Tern-like: Arctic to Antarctic)
    # Start: Greenland (70N, -40W)
    # Mid: West Africa (15N, -20W)
    # End: Antarctic (70S, 40E)
    
    lons = [-40, -20, 0, 40]
    lats = [70, 15, -30, -70]
    
    # Plot the migration path as a great circle/curved line in projection
    fig.plot(lons, lats, color='#dc2626', linewidth=2.5, marker='o', 
             markersize=5, transform=ccrs.Geodetic(), label='Migratory Route')
    
    # Add some text labels
    fig.text(-40, 72, 'Breeding Grounds', transform=ccrs.Geodetic(), fontweight='bold', color='#1e293b')
    fig.text(40, -75, 'Wintering Grounds', transform=ccrs.Geodetic(), fontweight='bold', color='#1e293b')
    
    fig.set_global()
    plt.title("Day 17: A New Tool - Global Migration via Cartopy", fontsize=22, pad=20, fontweight='bold')
    plt.legend(loc='lower left')
    
    output_path = os.path.join('2025', 'day_17', 'visualization', 'global_cartopy_migration.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 17: A new tool
A global migration map created using **Cartopy**, a powerful Python library for cartographic projections and geospatial data visualization. This "new tool" allows for sophisticated planetary-scale mapping, here showing a representative pole-to-pole migratory journey in a Robinson projection.

## Visualization
![Global Cartopy Migration](visualization/global_cartopy_migration.png)
"""
    with open(os.path.join('2025', 'day_17', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
