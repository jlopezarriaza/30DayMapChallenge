import os
from urllib.parse import urlencode
import requests
from utils import get_activities_for_year, plot_activities_on_map
from globals import AUTHORIZATION_BASE_URL, TOKEN_URL, API_URL, REDIRECT_URI


params = {
    "client_id": os.environ["STRAVA_CLIENT_ID"],
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": "activity:read_all",
}

authorization_url = AUTHORIZATION_BASE_URL + "?" + urlencode(params)
print("Visit the following URL to authorize your application:\n")
print(authorization_url)

authorization_code = input("Enter the authorization code from the url")

token_params = {
    "client_id": os.environ["STRAVA_CLIENT_ID"],
    "client_secret": os.environ["STRAVA_CLIENT_SECRET"],
    "code": authorization_code,
    "grant_type": "authorization_code",
}

token_response = requests.post(TOKEN_URL, data=token_params)
access_token = token_response.json()["access_token"]

activities_data = get_activities_for_year(
    access_token=access_token, years=[2020, 2021, 2022, 2023, 2024]
)
map = plot_activities_on_map(
    activities_data,
    color_by_type=True,
    default_opacities={
        "Run": 0.15,
        "Ride": 0.5,
        "Swim": 0.6,
        "Walk": 0.4,
    },
)
