import osmnx as ox
import matplotlib.pyplot as plt
import os

def main():
    print("Fetching Stow Lake area in Golden Gate Park...")
    # Center on Stow Lake
    center = (37.769, -122.478)
    tags = {'leisure': ['park', 'water'], 'natural': 'water'}
    gdf = ox.features_from_point(center, tags=tags, dist=400)
    
    print("Plotting with XKCD sketchy style...")
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(10, 10))
        fig.patch.set_facecolor('white')
        
        # Plot water (Stow Lake)
        gdf[gdf['natural'] == 'water'].plot(ax=ax, color='#a5f3fc', edgecolor='black', linewidth=1)
        
        # Plot islands/land
        gdf[gdf['leisure'] == 'park'].plot(ax=ax, color='#bbf7d0', edgecolor='black', linewidth=1, alpha=0.5)
        
        # Label the Heronry (Strawberry Hill island is a known spot)
        ax.text(-122.478, 37.769, 'Strawberry Hill', fontsize=12, ha='center')
        ax.text(-122.4785, 37.7685, 'Heronry (Nesting Birds!)', fontsize=14, color='#b91c1c', fontweight='bold', ha='center')
        
        # Add labels for surrounding features
        ax.text(-122.481, 37.771, 'The Lake', fontsize=12, rotation=45)
        ax.text(-122.475, 37.767, 'Walking Path', fontsize=10)
        
        ax.set_axis_off()
        ax.set_title('Analog Map: Great Blue Heron Nesting @ Stow Lake', fontsize=20, pad=20)
        
        output_path = os.path.join('2025', 'day_9', 'visualization', 'stow_lake_analog.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {output_path}")
        
    # Save a small README
    readme_content = f"""# Day 9: Analog
A "hand-drawn" sketch map of the Great Blue Heron nesting site (heronry) at Stow Lake in San Francisco's Golden Gate Park. Using the XKCD style to evoke an analog, field-note aesthetic.

## Visualization
![Stow Lake Analog](visualization/stow_lake_analog.png)
"""
    with open(os.path.join('2025', 'day_9', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
