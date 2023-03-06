import json
import requests

# take a points object and returns elevation data in form of json
def elevationApiResponse(pointsObj):
    apiEndPointLocal = "http://localhost/api/v2/lookup"
    apiEndPoint = "https://api.open-elevation.com/api/v1/lookup"
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(apiEndPointLocal, data=json.dumps(pointsObj), headers=header)
    jsonResult = response.json()
    return jsonResult['results'] # n*m  
    
# get elevation matrix
def getElevation(mat):
    '''- mat: Input Coordinate matrix'''
    n = len(mat)
    m = len(mat[0])
    locationDict = {'locations': []}

    count=0 

    listOfPoints=[]

    for i in range(n):
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
    responseList = elevationApiResponse(locationDict)
    listOfPoints.extend(responseList)

    idx = 0
    elevation_list = [] 
    landcover_list = []

    for i in range(n):
        row_elevation = []
        row_landcover = []
        for j in range(m):
            row_elevation.append(listOfPoints[idx]['elevation'])
            row_landcover.append(listOfPoints[idx]['landcover'])
            idx += 1
        elevation_list.append(row_elevation)
        landcover_list.append(row_landcover)

    return elevation_list, landcover_list

def getElevation_fromRaster(mat, elevation_dataset, landcover_dataset):
    n = len(mat)
    m = len(mat[0])

    elevation_list = [] 
    landcover_list = []

    for i in range(n):
        row_elevation = []
        row_landcover = []
        for j in range(m):
            temp = mat[i][j]
            # 'latitude': temp[0]
            # 'longitude': temp[1]
            row_elevation.append(elevation_dataset.lookup(temp[0],temp[1]))
            row_landcover.append(landcover_dataset.lookup(temp[0],temp[1]))
        elevation_list.append(row_elevation)
        landcover_list.append(row_landcover)
    return elevation_list, landcover_list

# 