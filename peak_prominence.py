import rasterio
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import copy

# Load the dem file
dem_file = "C:/Users/SAMARTH/Desktop/MTP/mtp/elevation/iit_mandi1.tif"
with rasterio.open(dem_file) as src:
    elevation_data = src.read(1)

print(np.max(elevation_data))
print("elevation _data shape: ", elevation_data.shape)

elevation_smooth1 = copy.deepcopy(elevation_data)
elevation_smooth2 = copy.deepcopy(elevation_data)
n, m = elevation_data.shape

def isPeak(elevation_smooth, i, j):
    if ((elevation_smooth[i][j] >= elevation_smooth[i-1][j]) and (elevation_smooth[i][j] >= elevation_smooth[i+1][j]) and (elevation_smooth[i][j] >= elevation_smooth[i][j-1]) and (elevation_smooth[i][j] >= elevation_smooth[i][j+1])):
        if ((elevation_smooth[i][j] >= elevation_smooth[i-1][j-1]) and (elevation_smooth[i][j] >= elevation_smooth[i+1][j+1]) and (elevation_smooth[i][j] >= elevation_smooth[i+1][j-1]) and (elevation_smooth[i][j] >= elevation_smooth[i-1][j+1])):
            # if ((elevation_smooth[i][j] >= elevation_smooth[i-2][j]) and (elevation_smooth[i][j] >= elevation_smooth[i+2][j]) and (elevation_smooth[i][j] >= elevation_smooth[i][j-2]) and (elevation_smooth[i][j] >= elevation_smooth[i][j+2])):
            #if ((elevation_smooth[i][j] >= elevation_smooth[i-2][j]) and (elevation_smooth[i][j] >= elevation_smooth[i+2][j]) and (elevation_smooth[i][j] >= elevation_smooth[i][j-2]) and (elevation_smooth[i][j] >= elevation_smooth[i][j+2])):
            # if not ((elevation_smooth[i][j] == elevation_smooth[i-1][j]) and (elevation_smooth[i][j] == elevation_smooth[i+1][j]) and (elevation_smooth[i][j] == elevation_smooth[i][j-1]) and (elevation_smooth[i][j] == elevation_smooth[i-1][j+1]) and (elevation_smooth[i][j] == elevation_smooth[i+1][j+1]) and (elevation_smooth[i][j] == elevation_smooth[i-1][j-1]) and (elevation_smooth[i][j] == elevation_smooth[i+1][j-1]) and (elevation_smooth[i][j] == elevation_smooth[i-1][j+1])):
                return True
    return False

# Smooth the elevation_map
passes = 1
for cnt in range(passes):
        for i in range(1, n-1):
                for j in range(1, m-1):
                        elevation_smooth1[i][j] = (elevation_smooth2[i-1][j] + elevation_smooth2[i+1][j] + elevation_smooth2[i][j-1] + elevation_smooth2[i][j+1] + elevation_smooth1[i][j])/5
        
        for i in range(1, n-1):
                for j in range(1, m-1):
                        elevation_smooth2[i][j] = (elevation_smooth1[i-1][j] + elevation_smooth1[i+1][j] + elevation_smooth1[i][j-1] + elevation_smooth1[i][j+1] + elevation_smooth1[i][j])/5

# Extract the contours from the elevation data
contour_levels = np.arange(100, np.max(elevation_data), 100) # adjust the levels as needed
sorted_contours = contour_levels[::-1]

# make contours
contours = []
sorted_contours_levels = []



# 
for level in sorted_contours:
    starting = len(contours)
    # print(level, "\n", len(contours))
    contours += measure.find_contours(elevation_data, level)
    ending = len(contours)
    # print(len(contours), "\n----------")
    for i in range(ending-starting):
        sorted_contours_levels.append(level)

# plot contours 
fig, ax = plt.subplots()
ax.imshow(elevation_data, interpolation='nearest', cmap=plt.cm.gray)
for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2, label=n) 
ax.axis('image')
plt.legend()
ax.set_xticks([])
ax.set_yticks([])
plt.show()


# get all peaks
peaks = []
peaks_lat = []
peaks_lon = []
max_elevation_contour = [0 for i in range(len(contours))]

# update max_elevation in each contour
for i in range(1, elevation_data.shape[0]-1):
    for j in range(1, elevation_data.shape[1]-1):
         if isPeak(elevation_smooth2, i, j):
              peaks.append([i, j])
              peaks_lat.append(i)
              peaks_lon.append(j)
              for k in range(len(contours)):
                   if measure.points_in_poly([(i,j)], contours[k]):
                        max_elevation_contour[k] = max(max_elevation_contour[k], elevation_data[i, j])

print("peaks: ", len(peaks))
print("peaks_lat: ", len(peaks_lat))
print("peaks_lon: ", len(peaks_lon))
# print(peaks)
plt.imshow(elevation_data, cmap="gray")
plt.scatter(peaks_lon, peaks_lat, color='r',s=1)
plt.show()



# get prominence for each peak
peak_prominences = [0 for i  in range(len(peaks)) ]
for peak_num in range(len(peaks)):
     for k in range(len(contours)):
            if measure.points_in_poly([peaks[peak_num]], contours[k]):
                 if max_elevation_contour[k] > elevation_data[peaks_lat[peak_num]][peaks_lon[peak_num]]:
                      peak_prominences[peak_num] = elevation_data[peaks_lat[peak_num]][peaks_lon[peak_num]] - sorted_contours_levels[k]
                      break
                 
print(peak_prominences)


"""
for contour in contours:
     print(len(contour))

# Sort the contours by decreasing maximum elevation value
# sorted_contours = sorted(contours, key=lambda contour: np.max(elevation_data[np.floor(contour[:, 0]).astype(int), np.floor(contour[:, 1]).astype(int)]), reverse=True)

# print("-----------")
# for contour in sorted_contours:
#      print(len(contour))
     
# Create an array to store the prominence values for each point in the elevation data
prominence_data = np.zeros_like(elevation_data)

# Iterate over each contour in the sorted list of contours
for contour in sorted_contours:
    # Find the maximum elevation value within the contour
    contour_mask = measure.grid_points_in_poly(elevation_data.shape, contour)
    max_elevation_contour = np.max(np.ma.masked_array(elevation_data, ~contour_mask))

    # Update the prominence values for each point in the contour
    for i in range(elevation_data.shape[0]):
        for j in range(elevation_data.shape[1]):
            if contour_mask[i, j] == True:
                # Calculate the prominence of the point
                prominence = max_elevation_contour - elevation_data[i, j]

                # Update the prominence value for the point
                prominence_data[i, j] = prominence

# Plot the prominence data
plt.imshow(prominence_data, cmap='viridis', vmax=np.percentile(prominence_data, 99))
plt.colorbar()
plt.show()

plt.imshow(elevation_data)
plt.show()
"""