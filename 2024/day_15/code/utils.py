from datetime import datetime

import folium
import polyline
import requests
from folium import plugins

api_url = "https://www.strava.com/api/v3"


def get_activities_for_year(access_token, years: list[int]):
    """
    Retrieve all Strava activities for a specified year.

    Parameters
    ----------
    access_token : str
        Strava API access token for authentication
    years : list[int]
        List of years for which to retrieve activities

    Returns
    -------
    list
        A list of dictionaries containing activity data from Strava API
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    start_date = datetime(min(years), 1, 1)
    end_date = datetime(max(years) + 1, 1, 1)

    after = int(start_date.timestamp())
    before = int(end_date.timestamp())

    all_activities = []
    page = 1
    while True:
        print(f"Getting activities for page {page}")
        activities_url = f"{api_url}/athlete/activities"
        params = {"per_page": 200, "page": page, "after": after, "before": before}

        activities_response = requests.get(activities_url, headers=headers, params=params)
        activities_data = activities_response.json()
        print(f"Got {len(activities_data)} activities")
        if not activities_data:
            break

        all_activities.extend(activities_data)
        page += 1

    return all_activities


def plot_activities_on_map(
    activities_data,
    color_by_type=True,
    default_opacities=None,
):
    """
    Create an interactive map visualization of Strava activities.

    Parameters
    ----------
    activities_data : list
        List of dictionaries containing Strava activity data
    color_by_type : bool, optional
        Whether to color-code activities by type (default is True)
    default_opacities : dict, optional
        Dictionary mapping activity types to their default opacity values
        Example: {'Run': 0.8, 'Ride': 0.3}

    Returns
    -------
    folium.Map
        A Folium map object with plotted activities
    """
    first_activity = activities_data[0]
    first_point = polyline.decode(first_activity["map"]["summary_polyline"])[0]
    m = folium.Map(location=first_point, zoom_start=12, tiles="cartodb positron")

    type_colors = {
        "Run": "firebrick",
        "Ride": "blue",
        "Swim": "cyan",
        "Walk": "green",
    }

    activity_groups = {}

    if default_opacities is None:
        default_opacities = {
            "Run": 0.15,
            "Ride": 0.75,
            "Swim": 0.6,
            "Walk": 0.4,
        }

    for activity in activities_data:
        if activity["map"]["summary_polyline"]:
            points = polyline.decode(activity["map"]["summary_polyline"])
            color = type_colors.get(activity["type"], "gray")

            if color_by_type:
                if activity["type"] not in activity_groups:
                    activity_groups[activity["type"]] = folium.FeatureGroup(
                        name=activity["type"]
                    )
                feature_group = activity_groups[activity["type"]]
            else:
                feature_group = m

            popup_html = f"""
                <b>{activity['name']}</b><br>
                Type: {activity['type']}<br>
                Distance: {activity['distance']/1000:.2f} km<br>
                Date: {activity['start_date_local']}<br>
            """

            opacity = default_opacities.get(activity["type"], 0.5)

            folium.PolyLine(
                points,
                weight=2,
                color=color,
                opacity=opacity,
                popup=folium.Popup(popup_html, max_width=300),
            ).add_to(feature_group)

    if color_by_type:
        for group in activity_groups.values():
            group.add_to(m)

    plugins.Fullscreen().add_to(m)

    opacity_control = """
    <script>
        function updateOpacity(value, activityType) {{
            var paths = document.querySelectorAll(`[data-activity="${{activityType}}"] path`);
            for(var i = 0; i < paths.length; i++) {{
                paths[i].style.opacity = value;
            }}
        }}
    </script>
    """.format(
        "\n".join(
            f'<label for="opacity-{activity_type}">{activity_type}:</label>'
            f'<input type="range" id="opacity-{activity_type}" min="0" max="1" step="0.1" '
            f'value="{default_opacities.get(activity_type, 0.5)}" '
            f"oninput=\"updateOpacity(this.value, '{activity_type}')\">"
            f"<br>"
            for activity_type in activity_groups.keys()
        )
    )

    m.get_root().html.add_child(folium.Element(opacity_control))
    m.save("visualization/activities_map.html")
    return m
