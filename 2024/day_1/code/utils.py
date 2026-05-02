# Third-party imports
import branca
import folium
import geopandas as gpd
import pandas as pd
import requests
from rtree import index
from shapely.geometry import Point, shape
from shapely.prepared import prep


def get_sf_fire_incidents() -> pd.DataFrame:
    """
    Fetch fire incident data from San Francisco's open data API.
    """
    api_endpoint = "https://data.sfgov.org/resource/wr8u-xric.json"
    api_params = {
        "$limit": 200000,
        "$offset": 0,
        "$where": "incident_date >= '2024-01-01' AND incident_date < '2024-12-31'",
    }
    api_response = requests.get(api_endpoint, params=api_params)
    api_response.raise_for_status()
    incidents_df = pd.DataFrame(api_response.json()).dropna(subset="point")

    # Extract latitude and longitude from the 'point' column
    incidents_df["latitude"] = incidents_df["point"].apply(
        lambda x: x["coordinates"][1]
    )  # Latitude is the second coordinate
    incidents_df["longitude"] = incidents_df["point"].apply(
        lambda x: x["coordinates"][0]
    )  # Longitude is the first coordinate

    return incidents_df
