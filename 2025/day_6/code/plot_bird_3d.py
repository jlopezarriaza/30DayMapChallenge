import pandas as pd
import pydeck as pdk
import requests
from io import StringIO
import os

def main():
    print("Fetching bird tracking data for 3D visualization...")
    url = "https://raw.githubusercontent.com/gabrieldluca/bird-migration/master/bird_tracking.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
    except Exception as e:
        print(f"Error: {e}")
        return

    # Sample data for performance (it's a large file)
    df = df.sample(5000).sort_values(['bird_name', 'date_time'])
    
    # Pydeck PathLayer expects a list of coordinates [[lon, lat, alt], ...]
    # We'll create paths for each bird
    bird_paths = []
    for bird in df['bird_name'].unique():
        bird_df = df[df['bird_name'] == bird]
        path = bird_df[['longitude', 'latitude', 'altitude']].values.tolist()
        # Scale altitude for visibility (meters to maybe something larger)
        scaled_path = [[p[0], p[1], p[2] * 10] for p in path] # 10x vertical exaggeration
        bird_paths.append({
            'name': bird,
            'path': scaled_path,
            'color': [255, 0, 0] if bird == 'Eric' else ([0, 255, 0] if bird == 'Nico' else [0, 0, 255])
        })

    print("Creating 3D map...")
    layer = pdk.Layer(
        "PathLayer",
        bird_paths,
        get_path="path",
        get_color="color",
        get_width=5000,
        width_min_pixels=2,
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=30,
        longitude=0,
        zoom=3,
        pitch=45,
        bearing=0
    )
    
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=pdk.map_styles.DARK)
    
    output_path = os.path.join('2025', 'day_6', 'visualization', 'bird_3d_paths.html')
    r.to_html(output_path)
    print(f"Saved to {output_path}")
    
    # Save a small README
    readme_content = f"""# Day 6: Dimensions
A 3D visualization of bird flight altitudes during migration. This map uses GPS tracking data for Lesser Black-backed Gulls, rendered with vertical exaggeration to highlight the vertical dimension of their journey.

## Visualization
[View Interactive 3D Map](visualization/bird_3d_paths.html)
"""
    with open(os.path.join('2025', 'day_6', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
