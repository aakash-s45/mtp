import requests as rq
import json
import threading
from threading import Thread
from time import sleep 

def func(variable, val):
      variable.append([0,val])
      print(f'variable {val} set to value: {variable}')


def multithread():
	MAX_THREAD = 4
    # creating list of size MAX_THREAD
	thread = list(range(MAX_THREAD))
    # creating MAX_THEAD number of threads
	variable = [[0,0], [0,1]]
	values = [0, 1, 2, 3]
	for i in range(MAX_THREAD):
		thread[i] = Thread(target=func, args=(variable, values[i]))
		thread[i].start()
                
    # Waiting for all threads to finish
	for i in range(MAX_THREAD):
		thread[i].join()

	print(f'variable final value is {variable}')

# multithread()


class foo:
    x = 0
    
def increase(foo):
    for i in range(3):
        print(f"[{threading.currentThread().getName()}] X is {foo.x}")
        foo.x += 1
        print(f"[{threading.currentThread().getName()}] X is now {foo.x} after increase")
        sleep(0.5)
        print(f"[{threading.currentThread().getName()}] X is now {foo.x} after sleep")
    return foo.x 

def testing():
    x = foo() 
    first = threading.Thread(name="Thread One", target=increase,args=([x]))
    second = threading.Thread(name="Thread Two", target=increase,args=([x]))
    
    first.start()
    second.start()
    
    first.join()
    second.join()  
    print(x.x)

# testing()






def elevationApiResponse(pointsObj,apiEndPoint):
    # apiEndPoint = "http://localhost/api/v1/lookup"
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = rq.post(apiEndPoint, data=json.dumps(pointsObj), headers=header)
    # return response
    jsonResult = response.json()
    return jsonResult['results'] # n*m  


def main():
	locationDict = {
		"locations":
		[
			{
				"latitude": -109.83007049344715, 
				"longitude": 44.36470033197011
			}
		]}
	coord = {
		'latitude': 31.58360498413924,
		'longitude': 77.43407308022033}
	# locationDict['locations'].append(coord)

	apiEndPoint = "http://localhost/api/v1/lookup"
	print(elevationApiResponse(locationDict,apiEndPoint))
	# apiEndPoint = "https://api.open-elevation.com//api/v1/lookup"
	# print(elevationApiResponse(locationDict,apiEndPoint))
	# 'https://api.open-elevation.com/api/v1/lookup?locations=10,10|20,20|41.161758,-8.583933'
	# apiEndPoint = "http://localhost:8080/api/v1/lookup"

	# apiEndPoint = 'http://localhost/api/v1/lookup?locations= 31.5836,77.4340'
	# response = rq.get(apiEndPoint)
	# if response.status_code==200:
	#     print(response.json())
	# else:
	#     print(response.status_code)



"""
import rasterio
from scipy.signal import find_peaks
import numpy as np



# Load the DEM file
dem_file = "C:/Users/SAMARTH/Desktop/MTP/mtp/elevation/iit_mandi1.tif"
with rasterio.open(dem_file) as src:
    dem = src.read(1)

# Find the highest peak in the DEM
peaks, _ = find_peaks(dem.ravel(), distance=20)
highest_peak = peaks[dem.ravel()[peaks].argmax()]

# Traverse the DEM to find the saddle
row, col = np.unravel_index(highest_peak, dem.shape)
while True:
    # Get the elevation values of the surrounding pixels
    elev = dem[max(0, row-1):min(row+2, dem.shape[0]), 
               max(0, col-1):min(col+2, dem.shape[1])]
    # Find the lowest elevation value
    min_elev = elev.min()
    # Check if the current pixel is the saddle
    if dem[row, col] == min_elev:
        saddle = row * dem.shape[1] + col
        break
    # Move to the pixel with the lowest elevation value
    row_offset, col_offset = np.unravel_index(elev.argmin(), elev.shape)
    row += row_offset - 1
    col += col_offset - 1

# Calculate the prominence of the peak
prominence = dem.ravel()[highest_peak] - dem.ravel()[saddle]
print(f"Prominence of the highest peak: {prominence:.2f} meters")
"""

"""
from skimage.feature import peak_local_max
from skimage import filters
import rasterio
import numpy as np
import matplotlib.pyplot as plt


# Open the DEM file using rasterio
dem_file = "C:/Users/SAMARTH/Desktop/MTP/mtp/elevation/iit_mandi1.tif"
with rasterio.open(dem_file) as src:
    # Read the raster data
    dem = src.read(1)

    # Smooth the DEM using a Gaussian filter
    dem_smooth = filters.gaussian(dem, sigma=3)

    # Find the local maxima in the smoothed DEM
    local_maxima = peak_local_max(dem_smooth, min_distance=5)

    # Find the saddle points in the smoothed DEM
    saddle_points = peak_local_max(-dem_smooth, min_distance=5)

    # Find the prominence of each peak
    prominences = []
    for peak in local_maxima:
        prominence = dem[peak[0], peak[1]] - np.max(dem_smooth[peak[0]-10:peak[0]+10, peak[1]-10:peak[1]+10])
        prominences.append(prominence)

    # Plot the DEM, local maxima, and saddle points
    fig, ax = plt.subplots()
    ax.imshow(dem, cmap='gray')
    ax.scatter(local_maxima[:, 1], local_maxima[:, 0], marker='o', s=20, c='r')
    ax.scatter(saddle_points[:, 1], saddle_points[:, 0], marker='o', s=20, c='b')
    ax.set_title('Local Maxima and Saddle Points')

    # Plot the prominences
    fig, ax = plt.subplots()
    ax.bar(range(len(prominences)), prominences)
    ax.set_xlabel('Peak Index')
    ax.set_ylabel('Prominence')
    ax.set_title('Peak Prominences')

    # Show the plots
    plt.show()
"""
