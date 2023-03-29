from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

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

api.add_resource(MyApi, '/name')

if __name__ == '__main__':
    app.run(debug=True)


# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f