import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import requests

def get_sf_fire_incidents():
    """Fetch fire incident data."""
    api_endpoint = "https://data.sfgov.org/resource/wr8u-xric.json"
    api_params = {"$limit": 5000, "$where": "incident_date >= '2024-01-01'"}
    response = requests.get(api_endpoint, params=api_params)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df = df.dropna(subset=['point'])
    df["lat"] = df["point"].apply(lambda x: x["coordinates"][1])
    df["lon"] = df["point"].apply(lambda x: x["coordinates"][0])
    return df

def main():
    print("Fetching fire incidents...")
    df = get_sf_fire_incidents()
    
    print("Plotting heat map...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')
    
    # Create the heatmap (KDE plot)
    sns.kdeplot(
        data=df, 
        x="lon", 
        y="lat", 
        cmap="hot", 
        fill=True, 
        thresh=0, 
        levels=100, 
        ax=ax,
        alpha=0.9
    )
    
    # Plot SF boundary for context
    import osmnx as ox
    city = ox.geocode_to_gdf("San Francisco, California, USA")
    city.plot(ax=ax, color='none', edgecolor='#333333', linewidth=1)
    
    ax.set_axis_off()
    ax.set_title('Thermal Intensity: SF Fire Incidents 2024', color='#ff4500', fontsize=24, pad=20, fontweight='bold')
    
    output_path = os.path.join('2024', 'day_25', 'visualization', 'sf_fire_heat.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#111111')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
