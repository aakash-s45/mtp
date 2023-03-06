import math 
import numpy as np
from copy import deepcopy
from numpy import array
import matplotlib.pyplot as plt
from dtocs import wDTDistance, initBinMap
from heapq import heapify, heappush, heappop

# kernel for neighbours 
# neighbours = [[-1, -1, -1, 0, 1, 1, 1, 0], [-1, 0, 1, -1, 1, 0, -1, 1]]
neighbours = [[-1,-1], [-1,0], [-1,1], [0,-1], [1,1], [1,0], [1,-1], [0,1]]
resistanceDict = {
    10 : 6, 	# Tree cover, green,
    20 : 5, 	# Shrubland, orange-yellow
    30 : 3, 	# Grassland, lemon-yellow
    40 : 4, 	# Cropland, pink ->5
    50 : 1, 	# Built-up, red
    60 : 2, 	# Bare / sparse vegetation, gray
    70 : 8, 	# Snow and ice, white, white
    80 : 10, 	# Permanent water bodies, blue
    90 : 9, 	# Herbaceous wetland, cyan
    95 : 10, 	# Mangroves, Strong cyan - lime green
    100 : 8 	# Moss and lichen, Very soft yellow (skin)
}

class cell:
    def __init__(self):
        self.parent_x = -1
        self.parent_y = -1
        self.f = 0
        self.g = 0
        self.h = 0
    def __init__(self, parent_x, parent_y, f, g, h):
        self.parent_x = parent_x
        self.parent_y = parent_y
        self.f = f
        self.g = g
        self.h = h



def isValid(i, j, n, m):
    if(i>=0 and i<n and j>=0 and j<m):
        return True
    return False


def astarFromSrcWithLC(elevation_map, landcover_map, src_latIdx, src_lonIdx, des_latIdx, des_lonIdx, res, alpha): 
    n, m = elevation_map.shape


    distFromSrc = initBinMap(src_latIdx, src_lonIdx, n, m)
    parentMat =  np.full((n, m, 2), [-1,-1])
    currDist = []
    heapify(currDist)
    heappush(currDist, [0, src_latIdx, src_lonIdx])

    while len(currDist) != 0:
        min_node = heappop(currDist)
        dist = min_node[0]
        curr_x = min_node[1]
        curr_y = min_node[2]
        
        for neigh in neighbours:
            new_x, new_y = curr_x+neigh[0], curr_y+neigh[1]
            if isValid(new_x, new_y, n, m):
                new_dist = dist + wDTDistance(elevation_map, curr_x, curr_y, new_x, new_y, res) + (alpha)*resistanceDict[landcover_map[new_x][new_y]]
                if new_dist < distFromSrc[new_x][new_y] :
                    parentMat[new_x][new_y] = [curr_x, curr_y]
                    if parentMat[new_x][new_y][0] == -1 or parentMat[new_x][new_y][1] == -1:
                        print("curr: ", curr_x, curr_y)
                        print("new: ", new_x, new_y)
                    distFromSrc[new_x][new_y] = new_dist
                    heappush(currDist,[new_dist, new_x, new_y])

    return distFromSrc, parentMat

def showPathDijkstra(elevation_map, parentMat, src_latIdx, src_lonIdx, des_latIdx, des_lonIdx):
    
    latIdx, lonIdx = des_latIdx, des_lonIdx
    path=[]

    temp_lat=0
    temp_lon=0
    while (latIdx!=src_latIdx) or (lonIdx!=src_lonIdx):
        temp_lat=latIdx
        temp_lon=lonIdx
        path.append([latIdx, lonIdx])
        latIdx = parentMat[temp_lat][temp_lon][0]
        lonIdx = parentMat[temp_lat][temp_lon][1]

    path_np_array=np.array(path)
    lat_list=path_np_array[:,0]
    lon_list=path_np_array[:,1]

    plt.imshow(elevation_map, cmap='gray')
    plt.scatter(lon_list, lat_list, color='r',s=1)
    plt.title("Dijkstra with res*0.125")
    plt.show()
        