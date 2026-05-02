import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests

def get_sf_fire_incidents():
    """Fetch fire incident data from San Francisco."""
    api_endpoint = "https://data.sfgov.org/resource/wr8u-xric.json"
    api_params = {
        "$limit": 10000, 
        "$where": "incident_date >= '2024-01-01' AND incident_date < '2024-12-31'",
    }
    response = requests.get(api_endpoint, params=api_params)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df = df.dropna(subset=['point'])
    df["latitude"] = df["point"].apply(lambda x: x["coordinates"][1])
    df["longitude"] = df["point"].apply(lambda x: x["coordinates"][0])
    
    # Extract hour from alarm_dttm (e.g., '2020-01-04T15:05:14.000')
    df['hour'] = pd.to_datetime(df['alarm_dttm']).dt.hour
    return df

def main():
    print("Fetching fire incidents...")
    df = get_sf_fire_incidents()
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326")
    
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    # Plot points colored by hour
    # Use 'twilight' colormap as it is cyclical (midnight is same as midnight)
    gdf.plot(
        ax=ax, 
        column='hour', 
        cmap='twilight', 
        markersize=5, 
        alpha=0.6,
        legend=True,
        legend_kwds={'label': "Hour of Day (0-23)", 'orientation': "horizontal", 'pad': 0.05}
    )
    
    ax.set_axis_off()
    ax.set_title('SF Fire Incidents 2024: Temporal Distribution', color='white', fontsize=20, pad=20)
    
    output_path = os.path.join('2024', 'day_12', 'visualization', 'sf_fire_time.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
