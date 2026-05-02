import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os
import ssl

def main():
    print("Preparing migratory path for projection comparison...")
    # Handle SSL for cartopy
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except:
        pass
        
    # Gannet-like transatlantic path
    lons = [-60, -30, -10, 5]
    lats = [45, 55, 60, 58]
    
    projections = [
        ('Mercator', ccrs.Mercator()),
        ('North Pole Stereographic', ccrs.NorthPolarStereo()),
        ('Orthographic (Global)', ccrs.Orthographic(central_longitude=-30, central_latitude=50))
    ]
    
    fig = plt.figure(figsize=(18, 6))
    fig.patch.set_facecolor('#f8fafc')
    
    for i, (name, proj) in enumerate(projections):
        ax = fig.add_subplot(1, 3, i+1, projection=proj)
        ax.add_feature(cfeature.LAND, facecolor='#f1f5f9')
        ax.add_feature(cfeature.OCEAN, facecolor='#e0f2fe')
        ax.add_feature(cfeature.COASTLINE, edgecolor='#94a3b8', linewidth=0.5)
        
        # Plot path
        ax.plot(lons, lats, color='#2563eb', linewidth=2, marker='o', markersize=4, transform=ccrs.Geodetic())
        
        ax.set_title(name, fontsize=16, fontweight='bold')
        
        # Set extent for Mercator and Stereo to focus on North Atlantic
        if name != 'Orthographic (Global)':
            ax.set_extent([-80, 20, 30, 80], crs=ccrs.PlateCarree())
            
    plt.suptitle("Day 19: Projections - Transatlantic Gannet Flight", fontsize=24, y=1.05, fontweight='black')
    plt.tight_layout()
    
    output_path = os.path.join('2025', 'day_19', 'visualization', 'migration_projections.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 19: Projections (GIS Day)
A comparison of three different map projections (Mercator, North Pole Stereographic, and Orthographic) showing the same transatlantic migratory path of a Northern Gannet. This visualization explores how projection choice influences our understanding of spatial relationships and the geometry of flight across the globe.

## Visualization
![Migration Projections](visualization/migration_projections.png)
"""
    with open(os.path.join('2025', 'day_19', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
