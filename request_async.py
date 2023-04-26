from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from main_raster import *
import json
import numpy as np
import yaml
from yaml.loader import SafeLoader
from flask_cors import CORS
import asyncio

# Load the config.yaml file
with open('./config.yaml','r') as f:
    config = yaml.load(f, Loader=SafeLoader)

    filePath = config['filePath']
    tileSize = int(config['tileSize'])
    SPLIT_DATA = bool(config['SPLIT_DATA'])
    alpha = float(config['alpha'])
    slope = float(config['slope'])
    h_weight = float(config['h_weight'])
    DEBUG = bool(config['DEBUG'])
    SHOW_PLOT = bool(config['SHOW_PLOT'])
    CSV_FILE = config['CSV_FILE']

app = Flask(__name__)
api = Api(app)
CORS(app)

# a test page for api which shows the available endpoint
@app.route('/')
def index():
    return "Available Endpoints: /get_path, /get_road, /get_peaks"

@app.route('/get_road', methods=['POST'])
async def get_road_handler():
    parser = reqparse.RequestParser()

    parser.add_argument('src_lat', type=float, required=True, help='Source Point Latitude')
    parser.add_argument('src_lon', type=float, required=True, help='Source Point Longitude')
    parser.add_argument('radius', type=float, required=True, help='Radius of Search')
    parser.add_argument('slope', type=float, required=True, help='Max Slope Allowed')
    parser.add_argument('h_weight', type=float, required=True, help='Horizontal Weightage')
    args = parser.parse_args()
    src_lat, src_lon = float(args['src_lat']),float(args['src_lon'])
    radius = float(args['radius'])
    slope = float(args['slope'])
    h_weight = float(args['h_weight'])
    
    # run the long running function in a separate task
    task = asyncio.create_task(PathToRoad((src_lat,src_lon), radius, par_dir=filePath,tile_size=tileSize,SPLIT_DATA=SPLIT_DATA,alpha=alpha,slope=slope,h_weight=h_weight,DEBUG=DEBUG,SHOW_PLOT=SHOW_PLOT))
    
    try:
        # wait for the task to complete or be cancelled
        result = await task
        if result is not None:
            path_list = result.tolist()
            return {'data': path_list},200
        else:
            return {'error': 'request cancelled'}, 500
    except asyncio.CancelledError:
        return {'error': 'request cancelled'}, 500

@app.route('/get_path', methods=['POST'])
async def get_path_handler():
    parser = reqparse.RequestParser()

    parser.add_argument('left', type=float, required=True, help='Left Coordinate of Bounding Box')
    parser.add_argument('bottom', type=float, required=True, help='Bottom Coordinate of Bounding Box')
    parser.add_argument('right', type=float, required=True, help='Right Coordinate of Bounding Box')
    parser.add_argument('top', type=float, required=True, help='Top Coordinate of Bounding Box')
    parser.add_argument('src_lat', type=float, required=True, help='Source Point Latitude')
    parser.add_argument('src_lon', type=float, required=True, help='Source Point Longitude')
    parser.add_argument('des_lat', type=float, required=True, help='Destination Point Latitude')
    parser.add_argument('des_lon', type=float, required=True, help='Destination Point Longitude')
    parser.add_argument('slope', type=float, required=True, help='Max Slope Allowed')
    parser.add_argument('h_weight', type=float, required=True, help='Horizontal Weightage')

    args = parser.parse_args()
    src_lat,src_lon = float(args['src_lat']),float(args['src_lon'])
    des_lat,des_lon = float(args['des_lat']),float(args['des_lon'])

    bounding_box = (float(args['left']),float(args['bottom']),float(args['right']),float(args['top']))
    slope = float(args['slope'])
    h_weight = float(args['h_weight'])
    
    # run the long running function in a separate task
    task = asyncio.create_task(main(bounding_box, (src_lat,src_lon), (des_lat,des_lon),par_dir=filePath,tile_size=tileSize,SPLIT_DATA=SPLIT_DATA,alpha=alpha,slope=slope,h_weight=h_weight,DEBUG=DEBUG,SHOW_PLOT=SHOW_PLOT))
    try:
        # wait for the task to complete or be cancelled
        result = await task
        if result is not None:
            path_list = result.tolist()
            return {'data': path_list},200
        else:
            return {'error': 'request cancelled'}, 500
    except asyncio.CancelledError:
        return {'error': 'request cancelled'}, 500
    
@app.route('/get_peaks', methods=['POST'])
async def get_peaks_handler():
    parser = reqparse.RequestParser()

    parser.add_argument('left', type=float, required=True, help='Left Coordinate of Bounding Box')
    parser.add_argument('bottom', type=float, required=True, help='Bottom Coordinate of Bounding Box')
    parser.add_argument('right', type=float, required=True, help='Right Coordinate of Bounding Box')
    parser.add_argument('top', type=float, required=True, help='Top Coordinate of Bounding Box')
    args = parser.parse_args()
    bounding_box = [float(args['left']),float(args['bottom']),float(args['right']),float(args['top'])]
    
    # run the long running function in a separate task
    task = asyncio.create_task(getPeaksFromCsv(csv_file = CSV_FILE, bbox = bounding_box))
    try:
        # wait for the task to complete or be cancelled
        result = await task
        if result is not None:
            return {'data': result},200
        else:
            return {'error': 'request cancelled'}, 500
    except asyncio.CancelledError:
        return {'error': 'request cancelled'}, 500

if __name__ == '__main__':
    app.run(debug=True)


# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f