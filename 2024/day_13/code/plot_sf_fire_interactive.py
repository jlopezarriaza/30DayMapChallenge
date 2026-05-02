import pandas as pd
import plotly.express as px
import requests
import os

def get_sf_fire_incidents():
    """Fetch fire incident data from San Francisco."""
    api_endpoint = "https://data.sfgov.org/resource/wr8u-xric.json"
    api_params = {
        "$limit": 5000, 
        "$where": "incident_date >= '2024-01-01'",
    }
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
    
    print("Creating interactive map with Plotly...")
    fig = px.scatter_mapbox(
        df, 
        lat="lat", 
        lon="lon", 
        color="primary_situation", 
        hover_name="address",
        hover_data=["incident_date", "battalion"],
        zoom=11, 
        height=800,
        title="SF Fire Incidents 2024 - Interactive Explorer"
    )
    
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    
    output_path = os.path.join('2024', 'day_13', 'visualization', 'sf_fire_interactive.html')
    fig.write_html(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
