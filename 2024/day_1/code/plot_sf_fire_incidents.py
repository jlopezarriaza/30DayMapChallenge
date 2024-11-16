from utils import get_sf_fire_incidents
if __name__ == "main":
    fire_incidents = get_sf_fire_incidents()



import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


google_terrain = cimgt.GoogleTiles(style="satellite")

fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
# Set the extent to focus on San Francisco
ax.set_extent([-122.511592, -122.319786, 37.616901, 37.829644], crs=ccrs.PlateCarree())
ax.scatter(fire_incidents['longitude'],fire_incidents['latitude'], s=0.1, color = 'firebrick', alpha= .1)
ax.add_image(google_terrain, 12)
plt.title('2024 Fire Incidents')

plt.savefig('fire_incidents.png',dpi=1200)
