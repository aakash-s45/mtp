import requests as rq
import json
from dtocs import *
# import numpy as np
# import math


def genMatrix(x1, y1, x2, y2, x_dist, y_dist):
    result = []
    temp_x = x1

    if (x1 < x2 and y1 < y2):
        while (temp_x < x2):
            row = []
            temp_y = y1
            while (temp_y < y2):
                temp_y += y_dist
                row.append([temp_x, temp_y])
            temp_x += x_dist
            result.append(row)

    elif (x1 > x2 and y1 < y2):
        while (temp_x > x2):
            row = []
            temp_y = y1
            while (temp_y < y2):
                temp_y += y_dist
                row.append([temp_x, temp_y])
            temp_x -= x_dist
            result.append(row)

    elif (x1 < x2 and y1 > y2):
        while (temp_x < x2):
            row = []
            temp_y = y1
            while (temp_y > y2):
                temp_y -= y_dist
                row.append([temp_x, temp_y])
            temp_x += x_dist
            result.append(row)

    elif (x1 > x2 and y1 > y2):
        while (temp_x > x2):
            row = []
            temp_y = y1
            while (temp_y > y2):
                temp_y -= y_dist
                row.append([temp_x, temp_y])
            temp_x -= x_dist
            result.append(row)

    return result


def getElevation(mat):
    n = len(mat)
    m = len(mat[0])
    locationDict = {'locations': []}
    apiEndPoint = "https://api.open-elevation.com/api/v1/lookup"
    # apiEndPoint = "http://localhost/api/v1/lookup"
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    for i in range(n):
        for j in range(m):
            temp = mat[i][j]

            coord = {
                'latitude': temp[0],
                'longitude': temp[1]}

            locationDict['locations'].append(coord)

    response = rq.post(apiEndPoint, data=json.dumps(
        locationDict), headers=header)

    jsonResult = response.json()
    print(jsonResult)
    listOfPoints = jsonResult['results'] # n*m
    idx = 0

    elevation_list = [] 

    for i in range(n):
        temp_row = []
        for j in range(m):
            temp_row.append(listOfPoints[idx]['elevation'])
            idx += 1
        elevation_list.append(temp_row)

    return elevation_list

def calcDistance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def initBinMap(x,y,n,m):
    res=[]
    for i in range(n):
        row=[]
        for j in range(m):
            row.append(math.inf)
        res.append(row)
    res[x][y]=0
    return res

def mainFun():

    # x1, y1 = 31.719, 76.946
    # x2, y2 = 31.735, 76.950

    x1, y1 = 31.808054, 77.037216
    x2, y2 = 31.837942, 77.045540

    coordinate_matrix = []
    # resolu 3 arc second
    xd = 1/3600
    yd = 1/3600

    coordinate_matrix = genMatrix(x1, y1, x2, y2, xd, yd)
    elevation_map = getElevation(coordinate_matrix)
    elevation_np_arr = np.array(elevation_map)
    n,m=elevation_np_arr.shape
    print(elevation_np_arr.shape)
    # print(elevation_np_arr)
    print("hello")
    # run the pass
    # 18,44

    # src_idx_x=2
    # src_idx_y=2

    # des_idx_x=55
    # des_idx_y=12

    src_idx_x, src_idx_y = 44.32480359458633, -109.81884898177093
    des_idx_x, des_idx_y = 44.30294042398075, -109.77537406272984

    bin_map_start = initBinMap(src_idx_x, src_idx_y, n, m)   
    # bin_map_end = initBinMap(des_idx_x, des_idx_y, n, m)

    # solve(elevation_np_arr, bin_map_start)
    # solve(elevation_np_arr, bin_map_end)

    parent_map = solve(elevation_np_arr, bin_map_start)

    # plt.imshow(bin_map_start,cmap='gray')
    # plt.show()
    # plt.imshow(bin_map_end,cmap='gray')
    # plt.show()



mainFun()




