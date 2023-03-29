from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from main_raster import *
import json
import numpy as np



app = Flask(__name__)
api = Api(app)

class MyApi(Resource):
    def get(self):
        return {'data': 'Hello World'},200
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', type=str, required=True, help='Enter your name')
        args = parser.parse_args()
        return {'data': f"Hello {args['name']}"},200

class PathList(Resource):
    def get(self):
        return {'data': 'Hi, This is a test api for MTP'},200
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('left', type=float, required=True, help='Left Coordinate of Bounding Box')
        parser.add_argument('bottom', type=float, required=True, help='Bottom Coordinate of Bounding Box')
        parser.add_argument('right', type=float, required=True, help='Right Coordinate of Bounding Box')
        parser.add_argument('top', type=float, required=True, help='Top Coordinate of Bounding Box')

        parser.add_argument('src_lat', type=float, required=True, help='Source Point Latitude')
        parser.add_argument('src_lon', type=float, required=True, help='Source Point Longitude')
        parser.add_argument('des_lat', type=float, required=True, help='Destination Point Latitude')
        parser.add_argument('des_lon', type=float, required=True, help='Destination Point Longitude')
        args = parser.parse_args()

        src_lat,src_lon = float(args['src_lat']),float(args['src_lon'])
        des_lat,des_lon = float(args['des_lat']),float(args['des_lon'])
        bounding_box = (float(args['left']),float(args['bottom']),float(args['right']),float(args['top']))
        # print(bounding_box)
        path = main(bounding_box, (src_lat,src_lon), (des_lat,des_lon))
        path_list = path.tolist()
        # json_str = json.dumps(path_list)

        return {'data': path_list},200
        # return {'data': "path list"},200

api.add_resource(MyApi, '/name')
api.add_resource(PathList, '/path')

if __name__ == '__main__':
    app.run(debug=True)


# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f