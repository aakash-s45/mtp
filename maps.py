from helper import *
from dtocs import distanceTransform
from getData import getElevation, getElevation_fromRaster
import numpy as np
from rasterio.plot import show
from matplotlib import pyplot as plt
from threading import Thread

class MapData:
    elevation_map = []
    landcover_map = []


def getGrayLevelMatrix(lon1, lat1, lon2, lat2, resolution=30):
    '''
        - Takes two points, then generate a matrix of coordinates and then calls api to get elevation 
        - resolution is in metres, default resolution = 30m
    '''
    # use these for testing
    # x1, y1 = 44.32480359458633, -109.81884898177093
    # x2, y2 = 44.30294042398075, -109.77537406272984
    coordinate_matrix = genMatrix(lat1, lon1, lat2, lon2, resolution)
    elevation_map, landcover_map = getElevation(coordinate_matrix) # using open elevation
    return np.array(elevation_map),np.array(landcover_map)


def getGrayLevelMatrixFromDataSet(lon1, lat1, lon2, lat2, elevation_dataset, landcover_dataset, resolution=30):
    '''
        - Takes two points, then generate a matrix of coordinates and then calls api to get elevation 
        - resolution is in metres, default resolution = 30m
    '''
    # use these for testing
    # x1, y1 = 44.32480359458633, -109.81884898177093
    # x2, y2 = 44.30294042398075, -109.77537406272984
    coordinate_matrix = genMatrix(lat1, lon1, lat2, lon2, resolution)
    elevation_map, landcover_map = getElevation_fromRaster(coordinate_matrix,elevation_dataset,landcover_dataset) # using open elevation
    return np.array(elevation_map),np.array(landcover_map)


def getElevationMultiThread(coordinate_matrix, elevation_dataset, landcover_dataset, start_row, elevation_map, landcover_map):
    n = len(coordinate_matrix)
    m = len(coordinate_matrix[0])

    for i in range(start_row, min(n, start_row + n//4 + 1)):                # assuming MAX_THREAD = 4
        for j in range(m):
            temp = coordinate_matrix[i][j]
            try:
                elevation_map[i][j] = elevation_dataset.lookup(temp[0],temp[1])
                landcover_map[i][j] = landcover_dataset.lookup(temp[0],temp[1])
            except:
                elevation_map[i][j] = 0
                landcover_map[i][j] = 0


def getGreyLevelMultiThread(lon1, lat1, lon2, lat2, elevation_dataset, landcover_dataset, resolution=30):
    '''
        - Takes two points, then generate a matrix of coordinates and then calls api to get elevation 
        - resolution is in metres, default resolution = 30m
    '''
    # use these for testing
    # x1, y1 = 44.32480359458633, -109.81884898177093
    # x2, y2 = 44.30294042398075, -109.77537406272984

    coordinate_matrix = genMatrix(lat1, lon1, lat2, lon2, resolution)

    MAX_THREAD = 4
    n = len(coordinate_matrix)
    m = len(coordinate_matrix[0])

    start_point = [((n//MAX_THREAD + 1) * i) for i in range(MAX_THREAD)]

    print('start points: ', start_point)

    elevation_map = [[0 for i in range(m)] for j in range(n)]
    landcover_map = [[0 for i in range(m)] for j in range(n)]

    thread = list(range(MAX_THREAD))
    for i in range(MAX_THREAD):
        thread[i] = Thread(target=getElevationMultiThread, args=(coordinate_matrix, elevation_dataset, landcover_dataset, start_point[i], elevation_map, landcover_map))
        thread[i].start()

    for i in range(MAX_THREAD):
        thread[i].join()

    return np.array(elevation_map), np.array(landcover_map)


def showRasterMap(elevation_map):
    fig, ax = plt.subplots(1, figsize=(12, 12))
    show(elevation_map, cmap='Greys_r', ax=ax)
    plt.title("Gray Level")
    plt.axis('off')
    plt.show()


