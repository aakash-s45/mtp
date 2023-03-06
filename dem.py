import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
dem = rio.open("../open-elevation/data/data_us.tif")
dem_array = dem.read(1).astype('float64')

print(dem_array)
# grey level
fig, ax = plt.subplots(1, figsize=(12, 12))
show(dem_array, cmap='Greys_r', ax=ax)
plt.axis('off')
plt.show()

# dem
fig, ax = plt.subplots(1, figsize=(12, 12))
show(dem_array, cmap='Greys_r', ax=ax)
show(dem_array, contour=True, ax=ax, linewidths=0.7)
plt.axis('off')
plt.show()

# red and blue
import richdem as rd
dem_richdem = rd.rdarray(dem_array, no_data=-9999)
dem_filled = rd.FillDepressions(dem_richdem, in_place=False)
dem_filled_fig = rd.rdShow(dem_filled, ignore_colours=[0], axes=False, cmap='jet', vmin=fig['vmin'], vmax=fig['vmax'], figsize=(16,10))