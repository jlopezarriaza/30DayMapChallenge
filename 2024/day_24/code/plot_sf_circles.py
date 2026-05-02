import pandas as pd
import h3
import matplotlib.pyplot as plt
import requests
import os

def get_sf_trees():
    """Fetch tree data."""
    api_endpoint = "https://data.sfgov.org/resource/tkzw-k3nq.json"
    api_params = {"$limit": 50000}
    response = requests.get(api_endpoint, params=api_params)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    return df.dropna(subset=['latitude', 'longitude']).astype({"latitude": "float64", "longitude": "float64"})

def main():
    print("Fetching tree data...")
    df = get_sf_trees()
    
    print("Binning into H3...")
    resolution = 9
    df['h3_cell'] = df.apply(lambda row: h3.latlng_to_cell(row['latitude'], row['longitude'], resolution), axis=1)
    
    counts = df['h3_cell'].value_counts().reset_index()
    counts.columns = ['h3_cell', 'tree_count']
    
    # Get centroids
    counts['latlng'] = counts['h3_cell'].apply(h3.cell_to_latlng)
    counts['lat'] = counts['latlng'].apply(lambda x: x[0])
    counts['lng'] = counts['latlng'].apply(lambda x: x[1])
    
    print("Plotting circle map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#000000')
    ax.set_facecolor('#000000')
    
    # Normalize sizes for circles
    max_count = counts['tree_count'].max()
    sizes = (counts['tree_count'] / max_count) * 100
    
    # Plot only circular shapes
    ax.scatter(
        counts['lng'], 
        counts['lat'], 
        s=sizes, 
        color='#00ff00', 
        alpha=0.6, 
        edgecolor='none'
    )
    
    ax.set_axis_off()
    ax.set_title('Circular SF: Street Tree Density', color='#00ff00', fontsize=22, pad=20)
    
    output_path = os.path.join('2024', 'day_24', 'visualization', 'sf_circles.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#000000')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
