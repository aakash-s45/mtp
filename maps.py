from helper import *
from dtocs import distanceTransform
from getData import getElevation, getElevation_fromRaster
import numpy as np
from rasterio.plot import show
from matplotlib import pyplot as plt


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

def showRasterMap(elevation_map):
    fig, ax = plt.subplots(1, figsize=(12, 12))
    show(elevation_map, cmap='Greys_r', ax=ax)
    plt.title("Gray Level")
    plt.axis('off')
    plt.show()


