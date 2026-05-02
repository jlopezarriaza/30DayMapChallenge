from pathlib import Path

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt

from utils import get_sf_fire_incidents


def main() -> None:
    fire_incidents = get_sf_fire_incidents()

    google_terrain = cimgt.GoogleTiles(style="satellite")
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Focus on San Francisco.
    ax.set_extent(
        [-122.511592, -122.319786, 37.616901, 37.829644],
        crs=ccrs.PlateCarree(),
    )
    ax.scatter(
        fire_incidents["longitude"],
        fire_incidents["latitude"],
        s=0.1,
        color="firebrick",
        alpha=0.1,
    )
    ax.add_image(google_terrain, 12)
    plt.title("2024 Fire Incidents")

    output_path = Path(__file__).resolve().parents[1] / "visualization" / "fire_incidents.png"
    plt.savefig(output_path, dpi=1200)


if __name__ == "__main__":
    main()
