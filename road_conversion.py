import osmium
import geopandas as gpd
import rasterio
from shapely.geometry import Point, LineString, box
from helper import  distanceBetwenPoints
import numpy as np
import matplotlib.pyplot as plt
from helper import findIndex
from tqdm import tqdm
from shapely.geometry import Point

class RoadHandler(osmium.SimpleHandler):
    def __init__(self):
        super(RoadHandler, self).__init__()
        self.lines = []

    def way(self, w):
        if 'highway' in w.tags:
            for i in range(1, len(w.nodes)):
                coords = [(w.nodes[i-1].lon, w.nodes[i-1].lat),
                          (w.nodes[i].lon, w.nodes[i].lat)]
                line = LineString(coords)
                length = distanceBetwenPoints(w.nodes[i-1].lat,w.nodes[i].lat,w.nodes[i-1].lon,w.nodes[i].lon)*1000
                self.lines.append({'geometry': line, 'highway': w.tags['highway'],'length': length,})

# Initialize the Osmium handler and apply it to the .osm.pbf file
def getRoadDataFrame(osm_file_path):
    osm_handler = RoadHandler()
    osmium_simple_walker = osmium.SimpleHandler()
    osmium_simple_walker.apply_file(osm_file_path, locations=True, idx='flex_mem')
    osm_handler.apply_file(osm_file_path, locations=True, idx='flex_mem')
    # Convert the lines to a GeoDataFrame
    lines_gdf = gpd.GeoDataFrame(osm_handler.lines, crs='EPSG:4326')
    return lines_gdf

def bresenham(x0, y0, x1, y1, arr):
    """
    Draw a line between two points in a numpy array using Bresenham's algorithm.

    arr: np.array
        The array to draw the line in.
    """
    dx = abs(x1 - x0)
    if x0<x1:
        sx = 1
    else:
        sx = -1
    dy = -abs(y1 - y0)
    if y0<y1:
        sy = 1
    else:
        sy = -1
    error = dx + dy
    
    while True:
        arr[x0, y0] = 110
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx
        
        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy


def addRoadInfoToLandcover(landcover_filePath, osm_file_path, outfile):

    def coordinatesToIndex(lon, lat, src, shape):
        # print((lon, lat))
        x, y = src.index(lon, lat)
        # print(x,y)
        h,w = shape
        if x<0:
            x = 0
        elif x >= h:
            x = h-1

        if y<0:
            y = 0
        elif y >= w:
            y = w-1
        return x, y


    # update the landcover file with the road information
    with rasterio.open(landcover_filePath) as src:
        bounds = src.bounds
        bbox = box(bounds.left, bounds.bottom, bounds.right, bounds.top)
        transform = src.transform
        landcover = src.read(1)
        meta = src.meta.copy()

        # print(landcover.max())
        # plt.imshow(landcover)
        # plt.show()

        # update {here}
        df = getRoadDataFrame(osm_file_path)
        # print(df.head())
        road_df = df['geometry']
        # print(road_df)
        road_segment_list = list(road_df)
        # plt.imshow(landcover)
        # plt.show()
        for line in tqdm(road_segment_list, desc="Adding Road Info"):
            p0,p1 = list(line.coords)

            if((bbox.contains(Point(p0)) and bbox.contains(Point(p1))) or bbox.contains(Point(p0)) or bbox.contains(Point(p1))):
                x0, y0 = coordinatesToIndex(p0[0],p0[1], src, landcover.shape)
                x1, y1 = coordinatesToIndex(p1[0],p1[1], src, landcover.shape)
                # print(x0, y0, x1, y1)

                # x0, y0 = findIndex(coords[0][1], coords[0][0], bounds.top, bounds.left, bounds.bottom, bounds.right, 30)
                # x1, y1 = findIndex(coords[1][1], coords[1][0], bounds.top, bounds.left, bounds.bottom, bounds.right, 30)
                bresenham(int(x0), int(y0), int(x1), int(y1), landcover)
        # plt.imshow(landcover)
        # plt.show()
        # save the updated data to new file
         # Open the output file
        with rasterio.open(outfile, 'w', **src.profile) as dst:
            # Write the modified data to the output file
            dst.write(landcover, 1)


if __name__ == '__main__':
    # # test
    # landcover_filePath = '/Users/aakash/Downloads/small_landcover.tif'
    # # osm_file_path = "/Users/aakash/Downloads/small.osm.pbf"
    # osm_file_path = "/Users/aakash/Downloads/north_campus.osm.pbf"
    # outfile = '/Users/aakash/Downloads/landcover_with_roads.tif'

    # rel
    landcover_filePath = '/Users/aakash/Desktop/MTP2/exp/landcover/landcover_data.tif'
    osm_file_path = "/Users/aakash/Downloads/northern-zone-latest.osm.pbf"
    outfile = '/Users/aakash/Downloads/landcover_with_roads_whole.tif'
    addRoadInfoToLandcover(landcover_filePath, osm_file_path, outfile)

