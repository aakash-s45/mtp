import requests as rq
import json
from dtocs import *
# import numpy as np
# import math

# latitude (north or south) always precedes longitude (east or west)

def getRadiusofEarth(lat_radian):
    r1=6378.137 #radius at equator
    r2=6356.752 #radius at poles
    a=r1*(math.cos(lat_radian))
    b=r2*(math.sin(lat_radian))
    num = (a*r1)**2 + (b*r2)**2
    den = a**2 + b**2
    rc=math.sqrt(num/den) #radius of earth at given latitude in km
    return rc*(math.cos(lat_radian)) #radius of ring at given latitude km

def getDegreeToMoveOnLat(resolution,latitude):
    # resolution in metres, latitude in degrees
    # moving on same latitude, (change in longitude)
    lat_rad=((math.pi)/180)*latitude
    rc=getRadiusofEarth(lat_rad)*1000 # in metre
    return (resolution*360)/(2*rc*math.pi)

def getDegreeToMoveOnLon(resolution):
    # resolution in metres, latitude in degrees
    # moving on same longitude, (change in latitude)
    r_earth=6371.001 # average radius of earth (in km)
    r_earth*=1000 # in metres
    return (resolution*360)/(2*r_earth*math.pi)


def genMatrix(lat1, lon1, lat2, lon2,res):
    result = []
    temp_lat = lat1
    lat_diff=getDegreeToMoveOnLon(res)

    if (lat1 < lat2 and lon1 < lon2):

        while (temp_lat < lat2):
            row = []
            temp_lon = lon1
            lon_diff=getDegreeToMoveOnLat(res,temp_lat)
            while (temp_lon < lon2):
                temp_lon += lon_diff
                row.append([temp_lat, temp_lon])
            temp_lat += lat_diff
            result.append(row)

    elif (lat1 > lat2 and lon1 < lon2):
        while (temp_lat > lat2):
            row = []
            temp_lon = lon1
            lon_diff=getDegreeToMoveOnLat(res,temp_lat)
            while (temp_lon < lon2):
                temp_lon += lon_diff
                row.append([temp_lat, temp_lon])
            temp_lat -= lat_diff
            result.append(row)

    elif (lat1 < lat2 and lon1 > lon2):
        while (temp_lat < lat2):
            row = []
            temp_lon = lon1
            lon_diff=getDegreeToMoveOnLat(res,temp_lat)
            while (temp_lon > lon2):
                temp_lon -= lon_diff
                row.append([temp_lat, temp_lon])
            temp_lat += lat_diff
            result.append(row)

    elif (lat1 > lat2 and lon1 > lon2):
        while (temp_lat > lat2):
            row = []
            temp_lon = lon1
            lon_diff=getDegreeToMoveOnLat(res,temp_lat)
            while (temp_lon > lon2):
                temp_lon -= lon_diff
                row.append([temp_lat, temp_lon])
            temp_lat -= lat_diff
            result.append(row)

    return result

def elevationApiResponse(pointsObj):
    apiEndPoint = "https://api.open-elevation.com/api/v1/lookup"
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = rq.post(apiEndPoint, data=json.dumps(pointsObj), headers=header)
    jsonResult = response.json()
    return jsonResult['results'] # n*m  
# get elevation data using API 
def getElevation(mat):
    n = len(mat)
    m = len(mat[0])
    locationDict = {'locations': []}

    count=0 

    listOfPoints=[]

    for i in range(n):
        # if(i not in range(51,101)):
        #     continue
        for j in range(m):
            count+=1
            temp = mat[i][j]
            coord = {
                'latitude': temp[0],
                'longitude': temp[1]}
            locationDict['locations'].append(coord)

            if(count==1500):
                responseList=elevationApiResponse(locationDict)
                locationDict['locations'].clear()
                listOfPoints.extend(responseList)
                count=0
    responseList=elevationApiResponse(locationDict)
    listOfPoints.extend(responseList)

    # print(len(listOfPoints))
    # return 
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
# initilize the binary map
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

      

    # x1, y1 = 31.779441, 76.966244
    # x2, y2 = 31.774567, 76.978456

    # x1, y1 = 31.808054, 77.037216
    # x2, y2 = 31.837942, 77.045540

    # x1, y1 = 31.778604, 77.019851
    # x2, y2 = 31.764229, 77.038477

    x1, y1 = 31.839224, 76.833049
    x2, y2 = 31.713527, 77.048941

    coordinate_matrix = []
    resolution = 120 # in metres

    coordinate_matrix = genMatrix(x1, y1, x2, y2,resolution)

    elevation_map = getElevation(coordinate_matrix)
    elevation_np_arr = np.array(elevation_map)
    n,m=elevation_np_arr.shape
    print(f"Gray Map Shape: {elevation_np_arr.shape}")
    # print(elevation_np_arr)

    # run the pass
    # 18,44

    src_idx_x=2
    src_idx_y=2

    des_idx_x=n-4
    des_idx_y=m-4

    bin_map_start = initBinMap(src_idx_x,src_idx_y,n,m)   
    bin_map_end = initBinMap(des_idx_x,des_idx_y,n,m)

    solve(elevation_np_arr, bin_map_start)
    solve(elevation_np_arr, bin_map_end)

    plt.imshow(elevation_map,cmap='gray')
    plt.title("Gray Level")
    plt.show()

    plt.imshow(bin_map_start,cmap='gray')
    plt.title("F1")
    plt.show()

    plt.imshow(bin_map_end,cmap='gray')
    plt.title("F2")
    plt.show()

mainFun()



