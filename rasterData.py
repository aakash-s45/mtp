import os
import math
import rasterio
import matplotlib.pyplot as plt
from rasterio.merge import merge
from shapely.geometry import box
from rasterio.mask import mask

def split_tif_into_tiles(tif_path, output_dir, tile_size=512):
    """
    This function splits a tif file into multiple tiles

    tif_path: Path to the tif file
    output_dir: Path to the output directory

    tile_size (optional): Size of the tiles in pixels
        default: 512
    """
    with rasterio.open(tif_path) as src:
        num_cols = src.width
        num_rows = src.height
        num_tiles_x = math.ceil(num_cols / tile_size)
        num_tiles_y = math.ceil(num_rows / tile_size)

        for tile_y in range(num_tiles_y):
            for tile_x in range(num_tiles_x):
                x1 = tile_x * tile_size
                y1 = tile_y * tile_size
                x2 = min(x1 + tile_size, num_cols)
                y2 = min(y1 + tile_size, num_rows)
                width = x2 - x1
                height = y2 - y1

                window = rasterio.windows.Window(x1, y1, width, height)
                transform = rasterio.windows.transform(window, src.transform)
                profile = src.profile.copy()
                profile.update({
                    'width': width,
                    'height': height,
                    'transform': transform,
                    'driver': 'GTiff'
                })

                # Read the tile data and write it to a new file
                tile_path = os.path.join(output_dir, f'tile_{tile_x}_{tile_y}.tif')
                with rasterio.open(tile_path, 'w', **profile) as dst:
                    data = src.read(window=window)
                    dst.write(data)

    print(f'{num_tiles_x} x {num_tiles_y} tiles created')



def mergeFiles(directory_path,merged_dataset_path, bbox):
    """
    This function merges the DEM files which intersect with the bounding box

    directory_path: Path to the directory containing the DEM files
    merged_dataset_path: Path to the merged dataset
    bbox: Bounding box coordinates (left, bottom, right, top)

    """
    # Get the bounding box coordinates
    minx, miny, maxx, maxy = bbox
    bbox = box(*bbox)
    # Get the DEM file paths within the bounding box
    dem_files = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.tif'):
            path = os.path.join(directory_path, filename)
            with rasterio.open(path) as src:
                # Check if the dataset intersects with the bounding box
                if bbox.intersects(box(*src.bounds)):
                    dem_files.append(path)
    
    # Merge the DEM files
    # print(dem_files)
    src_files_to_mosaic = [rasterio.open(path) for path in dem_files]
    mosaic, out_trans = merge(src_files_to_mosaic)
    
    merged_meta = src_files_to_mosaic[0].meta.copy()
    merged_meta.update({
        'width': mosaic.shape[2],
        'height': mosaic.shape[1],
        'transform': out_trans
    })
    
    with rasterio.open(merged_dataset_path, 'w', **merged_meta) as dst:
        dst.write(mosaic)
    
    # Close the source datasets
    for src in src_files_to_mosaic:
        src.close()
    
    print(f'{len(dem_files)} files merged')

def cropBoundingBox(merged_dem_file, outfile, bbox):
    with rasterio.open(merged_dem_file) as src:
    # Get the window of the bounding box
        window = src.window(*bbox)
        data = src.read(window=window)
        # Get the metadata of the window
        transform = rasterio.windows.transform(window, src.transform)

        meta = src.meta.copy()
        meta.update({
            'width': data.shape[1],
            'height': data.shape[0],
            'transform': transform
        })
        meta['width'], meta['height'] = data.shape[1], data.shape[0]
    
        # # Compute the affine transform of the window
        
        with rasterio.open(outfile, 'w', **meta) as dst:
            dst.write(data)
    

def show_dem(filepath,cmap='terrain'):
    with rasterio.open(filepath) as src:
        raster = src.read(1)
    plt.imshow(raster, cmap = cmap)
    plt.show()

def indexToCoordinates(dem_path,row,col):
    """
    This function converts the row and column index to coordinates

    dataset: The dataset
    row: Row index
    col: Column index
    """
    with rasterio.open(dem_path) as dataset:
        # Convert the pixel coordinates to geographic coordinates
        lon, lat = dataset.xy(row, col)
        # Print the geographic coordinates
        print(lon, lat)
    
def coordinatesToIndex(dem_path,lon,lat):
    """
    This function converts the coordinates to row and column index

    dataset: The dataset
    lon: Longitude
    lat: Latitude
    """
    with rasterio.open(dem_path) as dataset:
        # Convert the geographic coordinates to pixel coordinates
        row, col = dataset.index(lon, lat)
        # Print the pixel coordinates
        print(row, col)


def bounding_boxes_intersect(bbox1, bbox2):
    """
    Check if two bounding boxes intersect.
    
    Args:
        bbox1 (tuple): Tuple of bounding box coordinates in the format (left, bottom, right, top).
        bbox2 (tuple): Tuple of bounding box coordinates in the format (left, bottom, right, top).
    
    Returns:
        bool: True if the bounding boxes intersect, False otherwise.
    """
    left1, bottom1, right1, top1 = bbox1
    left2, bottom2, right2, top2 = bbox2
    
    box1 = box(left1, bottom1, right1, top1)
    box2 = box(left2, bottom2, right2, top2)
    
    return box1.intersects(box2)

def getDataBoundingBox(filepath, bbox):
    with rasterio.open(filepath) as src:
    # Get the window of the bounding box
        window = src.window(*bbox)
        data = src.read(window=window)
        # Get the metadata of the window
        meta = src.meta.copy()
        meta['width'], meta['height'] = data.shape[1], data.shape[0]
        # # Compute the affine transform of the window
        transform = rasterio.windows.transform(window, src.transform)
        return (data,src.bounds,src.transform)

        
def plot_multiband_raster(raster_file,bbox):
    """Read a multiband raster file using rasterio and plot the output using Matplotlib.
    
    Args:
        raster_file (str): Path to the raster file.
    """
    # Open the raster file using rasterio
    with rasterio.open(raster_file) as src:
        # Read all the bands of the raster
        window = src.window(*bbox)
        bands = src.read(window=window)
        
        # Get the metadata of the raster
        metadata = src.profile
    
    # Plot each band of the raster using Matplotlib
    num_bands = bands.shape[0]
    fig, axes = plt.subplots(ncols=num_bands, figsize=(6*num_bands, 6))
    for i in range(num_bands):
        ax = axes[i] if num_bands > 1 else axes
        c_map = ['gray','terrain']
        ax.imshow(bands[i], cmap=c_map[i])
        ax.set_title(f'Band {i+1}')
        ax.axis('off')
        
    # Add a title to the plot
    title = f'{metadata["driver"]} raster ({metadata["width"]}x{metadata["height"]})\n{num_bands} bands, {metadata["dtype"]}'
    fig.suptitle(title, fontsize=16, y=1.05)
    
    # Show the plot
    plt.show()


def get_resolution(raster_file):
    with rasterio.open(raster_file) as src:
        transform = src.transform
        # calculate the resolution in degrees
        x_res_deg = abs(transform[0])
        y_res_deg = abs(transform[4])

        # Get the center latitude of the dataset
        center_lat = (src.bounds.top + src.bounds.bottom) / 2

        # Calculate the length of one degree of longitude and latitude at the center latitude
        lon_deg_to_m = math.cos(center_lat * math.pi / 180) * 111320
        lat_deg_to_m = 111133

        # Convert the pixel resolution from degrees to meters
        x_res_m = x_res_deg * lon_deg_to_m
        y_res_m = y_res_deg * lat_deg_to_m
        
        avg_res = (x_res_m + y_res_m)/2
        return (avg_res, x_res_deg, y_res_deg)

def get_coordinate_at_position(arr, row_num, col_num, bbox):
    xmin, ymin, xmax, ymax = bbox
    rows, cols = arr.shape
    
    # Calculate the pixel sizes in x and y directions
    xres = (xmax - xmin) / cols
    yres = (ymax - ymin) / rows
    
    # Calculate the latitude and longitude of the specified position
    if ymin < ymax:
        lat = ymax - (row_num * yres) - (yres / 2)
    else:
        lat = ymin + (row_num * yres) + (yres / 2)
    
    if xmin < xmax:
        lon = xmin + (col_num * xres) + (xres / 2)
    else:
        lon = xmax - (col_num * xres) - (xres / 2)
    
    return lat, lon

def get_position_at_coordinate(arr, lat, lon, bbox):
    xmin, ymin, xmax, ymax = bbox
    rows, cols = arr.shape
    
    # Calculate the pixel sizes in x and y directions
    xres = (xmax - xmin) / cols
    yres = (ymax - ymin) / rows
    
    # Calculate the row and column indices of the specified position
    if ymin < ymax:
        row_num = int((ymax - lat) // yres)
    else:
        row_num = int((lat - ymin) // yres)
    
    if xmin < xmax:
        col_num = int((lon - xmin) // xres)
    else:
        col_num = int((xmax - lon) // xres)
    
    return row_num, col_num


