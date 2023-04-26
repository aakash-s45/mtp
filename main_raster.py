from dijkstra import showPath, generatePath, dijkstraFromSrcToRoad
from astar import astarFromSrcWholeBB, astarFromSrcTillDes
from rasterData import *
from helper import findIndex
import numpy as np
import asyncio



def main(bbox, src_coordinates, dest_coordinates, par_dir, tile_size = 512, alpha = 0, h_weight=0.1, slope=40,resolution=30, SPLIT_DATA = False,  DEBUG = False, SHOW_PLOT = False):
    """
    bbox: bounding box of the area of interest (left, bottom, right, top)
    resolution: Resolution of the DEM in meters
    src_coordinates: Source coordinates (latitude, longitude)
    dest_coordinates: Destination coordinates (latitude, longitude)

    """
    try:

        map_data_tif_path = par_dir + '/data/merged_w_RW.tif'
        split_data_dir = par_dir + '/data/tile_data_water'
        merged_data_path  = par_dir + '/data/temp/file.tif'

        # create subdirectories if they don't exist
        if not os.path.exists(split_data_dir):
            os.makedirs(split_data_dir)
        if not os.path.exists(par_dir + '/data/temp'):
            os.makedirs(par_dir + '/data/temp')

        x_res,y_res = resolution, resolution

        # top left and bottom right coordinates
        # bbox: left bottom right top
        lat1, lon1 = bbox[3], bbox[0]
        lat2, lon2 = bbox[1], bbox[2]

        if(SPLIT_DATA):
            split_tif_into_tiles(map_data_tif_path, split_data_dir, tile_size)

        mergeFiles(split_data_dir, merged_data_path, bbox)
        resolution, x_res, y_res = get_resolution(merged_data_path)

        map_data, bounds, tf = getDataBoundingBox(merged_data_path, bbox)

        if SHOW_PLOT:
            plot_multiband_raster(merged_data_path,bbox)
        if DEBUG:
            print("Elevation Map Info")
            print(f"Gray Map Shape: {map_data[0].shape}")
            print(f"Min: {map_data[0].min()}")
            print(f"Max: {map_data[0].max()}")

        src_lat, src_lon = src_coordinates
        des_lat, des_lon = dest_coordinates

        src_latIdx,src_lonIdx = findIndexFromCoordinate(bbox, map_data[0], src_lon, src_lat)
        des_latIdx,des_lonIdx = findIndexFromCoordinate(bbox, map_data[0], des_lon, des_lat)

        # src_latIdx,src_lonIdx = get_position_at_coordinate(map_data[0], src_lat, src_lon, bbox)
        # des_latIdx,des_lonIdx = get_position_at_coordinate(map_data[0], des_lat, des_lon, bbox)

        distFromSrc, parentMat  = astarFromSrcTillDes(map_data[0], map_data[1], src_latIdx, src_lonIdx, des_latIdx, des_lonIdx, alpha, h_weight, resolution, slope)

        if SHOW_PLOT:
            plt.imshow(distFromSrc,cmap='gray')
            plt.title("Distance from Source")
            plt.show()

            showPath(map_data[0], parentMat, src_latIdx, src_lonIdx, des_latIdx, des_lonIdx,alpha,h_weight,resolution,slope)

        path_array = generatePath(map_data[0], parentMat, (src_latIdx,src_lonIdx), (des_latIdx,des_lonIdx))

        def convertToCoordinates(x):
            return get_coordinate_at_position(map_data[0], x[0], x[1], bbox)

        return np.apply_along_axis(convertToCoordinates, 1, path_array)
    except asyncio.CancelledError:
        # catch the CancelledError exception and exit the function
        return None

def PathToRoad(src_coordinates, radius, par_dir, tile_size = 512, alpha = 0, h_weight=0.1, slope=40,resolution=30, SPLIT_DATA = False,  DEBUG = False, SHOW_PLOT = False):
    """
    resolution: Resolution of the DEM in meters
    src_coordinates: Source coordinates (latitude, longitude)

    """
    try:
        map_data_tif_path = par_dir + '/data/merged_file_w_roads.tif'
        split_data_dir = par_dir + '/data/tile_data_water'
        merged_data_path  = par_dir + '/data/temp/file.tif'

        # create subdirectories if they don't exist
        if not os.path.exists(split_data_dir):
            os.makedirs(split_data_dir)
        if not os.path.exists(par_dir + '/data/temp'):
            os.makedirs(par_dir + '/data/temp')

        x_res,y_res = resolution, resolution

        # top left and bottom right coordinates
        # bbox: left bottom right top
        src_lat, src_lon = src_coordinates
        bbox = getBoundingBoxFromAPoint(src_lat, src_lon, 30)

        lat1, lon1 = bbox[3], bbox[0]
        lat2, lon2 = bbox[1], bbox[2]

        if(SPLIT_DATA):
            split_tif_into_tiles(map_data_tif_path, split_data_dir, tile_size)

        mergeFiles(split_data_dir, merged_data_path, bbox)
        resolution, x_res, y_res = get_resolution(merged_data_path)

        map_data, bounds, tf = getDataBoundingBox(merged_data_path, bbox)

        if SHOW_PLOT:
            plot_multiband_raster(merged_data_path,bbox)
        if DEBUG:
            print("Elevation Map Info")
            print(f"Gray Map Shape: {map_data[0].shape}")
            print(f"Min: {map_data[0].min()}")
            print(f"Max: {map_data[0].max()}")


        src_latIdx,src_lonIdx = findIndexFromCoordinate(bbox, map_data[0], src_lon, src_lat)

        distFromSrc, parentMat, (des_latIdx, des_lonIdx) = dijkstraFromSrcToRoad(map_data[0], map_data[1], src_latIdx, src_lonIdx,alpha,h_weight,resolution,slope)


        def convertToCoordinates(x):
            return get_coordinate_at_position(map_data[0], x[0], x[1], bbox)

        if(des_latIdx!=-1 and des_lonIdx!=-1):
            if SHOW_PLOT:
                plt.imshow(distFromSrc,cmap='gray')
                plt.title("Distance from Source")
                plt.show()

                showPath(map_data[0], parentMat, src_latIdx, src_lonIdx, des_latIdx, des_lonIdx,alpha,h_weight,resolution,slope)

            path_array = generatePath(map_data[0], parentMat, (src_latIdx,src_lonIdx), (des_latIdx,des_lonIdx))

            return np.apply_along_axis(convertToCoordinates, 1, path_array)
        else:
            return np.array([])
            
    except asyncio.CancelledError:
        # catch the CancelledError exception and exit the function
        return None
    

if __name__ == "__main__":
    par_dir = "/Users/aakash/Desktop/MTP2/code"
    tile_size = 512
    SPLIT_DATA = False

    alpha = 0
    h_weight = 0.1
    slope = 40
    resolution = 30 

    src_lat, src_lon = 31.733824874811024, 77.00073130455512
    des_lat, des_lon = 31.726524680775725, 77.00802691307562
    bounding_box = (76.98328796870653,31.70144173323603, 77.01350037105028,31.737946830245892)
    path = main(bounding_box, (src_lat,src_lon), (des_lat,des_lon), par_dir = par_dir, tile_size=tile_size,SPLIT_DATA=SPLIT_DATA,alpha=alpha,h_weight=h_weight,slope=slope,resolution=resolution, DEBUG=True, SHOW_PLOT=True)
    print(path)
    

    






