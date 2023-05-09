import math 
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from helper import neighbourDist, LandcoverInfo

# kernel for forward and backward pass 
fmask = [[-1, -1, -1, 0], [-1, 0, 1, -1]]
bmask = [[1, 1, 1, 0], [1, 0, -1, 1]]


def wDTDistance(mat, x1, y1, x2, y2, h_weight, res=30):
    """weighted distance between two points (eucledien distance)"""
    if((abs(x1-x2)==1 and abs(y1-y2)==0) or (abs(x1-x2)==0 and abs(y1-y2)==1)):
        return ((mat[x1][y1] - mat[x2][y2])**2 + (h_weight*res)**2) ** 0.5
        # return ((mat[x1][y1] - mat[x2][y2])**2 + 1) ** 0.5
    elif(abs(x1-x2)==1 and abs(y1-y2)==1):
        return ((mat[x1][y1] - mat[x2][y2])**2 + (h_weight*res*(2**0.5))**2) ** 0.5
        # return ((mat[x1][y1] - mat[x2][y2])**2 + 2) ** 0.5


def initBinMap(i, j, n, m):
    """ Initialize binary map of given size"""
    res = []
    for x in range(n):
        row = []
        for y in range(m):
            row.append(math.inf)
        res.append(row)
    res[i][j] = 0
    return res
    
def distanceTransform(elevation_map, landcover_map, bin_map, accuracy, alpha=0, h_weight=0, res=30, slope = 30):
    """ Apply forward and backward pass on the given binary map using gray map"""
    global fmask
    global bmask
    n, m = elevation_map.shape
    numPass = 0
    limit = 25
    parentMat =  np.full((n, m,2), [-1,-1])
    notConverged = True
    slope = (slope * math.pi) / 180
    
    while notConverged:
        numPass += 1
        notConverged = False

        # forward pass
        for row in range(1, n-1):
            for col in range(1, m-1):
                for cnt in range(0, 4):
                    row_prev = row + fmask[0][cnt]
                    col_prev = col + fmask[1][cnt]
                    horizontal_dist = neighbourDist(row, col, row_prev, col_prev, res)
                    if (abs(elevation_map[row][col] - elevation_map[row_prev][col_prev]) / horizontal_dist) <= math.tan(slope):
                        
                        new_dist = bin_map[row_prev][col_prev] + wDTDistance(elevation_map, row, col, row_prev, col_prev, h_weight, res) + (alpha)*LandcoverInfo().resistanceDict[landcover_map[row][col]]
                        if new_dist < bin_map[row][col]:
                            if bin_map[row][col]-new_dist > accuracy:
                                notConverged = True
                            bin_map[row][col] = new_dist
                            parentMat[row][col] = [row_prev, col_prev]
        # backward pass
        for row in range(n-2, 0, -1):
            for col in range(m-2, 0, -1):
                for cnt in range(0, 4):
                    row_prev = row + bmask[0][cnt]
                    col_prev = col + bmask[1][cnt]
                    horizontal_dist = neighbourDist(row, col, row_prev, col_prev, res)
                    if (abs(elevation_map[row][col] - elevation_map[row_prev][col_prev]) / horizontal_dist) <= math.tan(slope):

                        new_dist = bin_map[row_prev][col_prev] + wDTDistance(elevation_map, row, col, row_prev, col_prev, h_weight, res) + (alpha)*LandcoverInfo().resistanceDict[landcover_map[row][col]]
                        if new_dist < bin_map[row][col]:
                            if bin_map[row][col]-new_dist > accuracy:
                                notConverged = True
                            bin_map[row][col] = new_dist
                            parentMat[row][col] = [row_prev, col_prev]
        if numPass == limit:
            break
    print(f"Number of Passes for convergence: {numPass}")
    return parentMat



def applyDistTfDoubleImg(elevation_map, landcover_map, bin_map_start, bin_map_end, accuracy=0.001, alpha=0, h_weight=0, res=30, slope = 30):
    print("Applying Distance transform double image......")
    distanceTransform(elevation_map, landcover_map, bin_map_start, accuracy, alpha, h_weight, res, slope)
    distanceTransform(elevation_map, landcover_map, bin_map_end, accuracy, alpha, h_weight, res, slope)
    print("Done!")

def applyDistTfSingleSource(elevation_map, landcover_map, bin_map_start, accuracy=0.001, alpha=0, h_weight=0, res=30, slope = 30):
    print("Applying Distance transform single image......")
    parentMat = distanceTransform(elevation_map, landcover_map, bin_map_start, accuracy, alpha, h_weight, res, slope)
    print("Done!")
    return parentMat
        

def combineBinmap(bin_map_start,bin_map_end):
    bin_map_combined = deepcopy(bin_map_start)
    n = len(bin_map_combined)
    m = len(bin_map_combined[0])

    for i in range(n):
        for j in range(m):
            bin_map_combined[i][j] = bin_map_start[i][j] + bin_map_end[i][j]

    return bin_map_combined

def generatePath(bin_map_combined):
    np_bin_combined=np.array(bin_map_combined)
    n,m=np_bin_combined.shape
    minval = np_bin_combined.min()
    for i in range(n):
        for j in range(m):
            if np_bin_combined[i][j]!=math.inf and  round(np_bin_combined[i][j],5)==round(minval,5):
                np_bin_combined[i][j]=math.inf

    return np_bin_combined

def showPathUsingParents(elevation_map, parentMat, src_latIdx, src_lonIdx, des_latIdx, des_lonIdx, alpha, h_weight, res, slope):
    
    latIdx, lonIdx = des_latIdx, des_lonIdx
    path = []
    while (latIdx!=src_latIdx) or (lonIdx!=src_lonIdx):
        temp_lat = latIdx
        temp_lon = lonIdx
        path.append([latIdx, lonIdx])
        latIdx = parentMat[temp_lat][temp_lon][0]
        lonIdx = parentMat[temp_lat][temp_lon][1]

    path_np_array=np.array(path)
    lat_list=path_np_array[:,0]
    lon_list=path_np_array[:,1]

    plt.imshow(elevation_map, cmap='gray')
    plt.scatter(lon_list, lat_list, color='r',s=1)
    # plt.title(F"DTOCS (single image) with res*{h_weight}")
    plt.title(f"DTOCS (single image) -> alpha:{alpha}, h_weight:{h_weight}, res:{res}, slope:{slope}")
    plt.show()

def showPathDoubleImg(elevation_map, combined_bin_map, h_weight):
    
    n,m = combined_bin_map.shape
    minval = combined_bin_map.min()
    path=[]

    for i in range(n):
        for j in range(m):
            if combined_bin_map[i][j]!=math.inf and  round(combined_bin_map[i][j],5)==round(minval,5):
            # if combined_bin_map[i][j]!=math.inf and  round(combined_bin_map[i][j],11)==round(minval,11):
            # if np_bin_combined[i][j]!=math.inf and  np_bin_combined[i][j]==minval:
                path.append([i, j])

    path_np_array=np.array(path)
    lat_list=path_np_array[:,0]
    lon_list=path_np_array[:,1]

    plt.imshow(elevation_map, cmap='gray')
    plt.scatter(lon_list, lat_list, color='r',s=1)
    plt.title(f"DTOCS (double image) with res*{h_weight}")
    plt.show()
    
    
