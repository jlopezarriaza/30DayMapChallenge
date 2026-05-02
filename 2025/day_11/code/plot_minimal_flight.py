import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    print("Generating minimalist flight curve...")
    # A single line representing a wingbeat or a soaring trajectory
    x = np.linspace(0, 10, 500)
    y = np.sin(x) * np.exp(-x/5) # Dampened oscillation (a bird settling into a glide)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Plot the minimal line
    ax.plot(x, y, color='black', linewidth=1.5)
    
    # Add a tiny "eye" or "head" circle at the end to hint it's a bird
    ax.scatter([x[-1]], [y[-1]], color='black', s=10)
    
    ax.set_axis_off()
    
    # Minimal text
    ax.text(0.5, 0.05, "FLIGHT #11", transform=ax.transAxes, ha='center', fontsize=8, color='#999999')
    
    output_path = os.path.join('2025', 'day_11', 'visualization', 'minimal_flight.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 11: Minimal map
A radical minimalist representation of a bird's flight trajectory. This "map" consists of a single line capturing the rhythmic oscillation of a wingbeat as it transitions into a glide.

## Visualization
![Minimal Flight](visualization/minimal_flight.png)
"""
    with open(os.path.join('2025', 'day_11', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
