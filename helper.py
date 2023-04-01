import math

def getRadiusofEarth(lat_radian):
    """ Get radius of earth at given latitude km """
    r1 = 6378.137     #radius at equator
    r2 = 6356.752     #radius at poles
    a = r1 * (math.cos(lat_radian))
    b = r2 * (math.sin(lat_radian))
    num = (a * r1)**2 + (b * r2)**2
    den = a**2 + b**2
    return math.sqrt(num / den)     #radius of earth at given latitude in km
    
# def getDegreeToMoveOnLat(resolution,latitude):
def changeInLongitude(resolution, latitude):
    '''- resolution in metres, latitude in degrees
       - moving on same latitude, (change in longitude)'''
    lat_rad = ((math.pi) / 180) * latitude     # convert to radian    
    r_earth = getRadiusofEarth(lat_rad) # radius of earth at given latitude
    r_ring = r_earth * (math.cos(lat_rad)) *1000 #radius of ring at given latitude km
    return (resolution * 360) / (2 * r_ring * math.pi)
    
# def getDegreeToMoveOnLon(resolution):
def changeInLatitude(resolution, latitude):
    """ - resolution in metres, latitude in degrees
        - moving on same longitude, (change in latitude) """
    lat_rad = ((math.pi) / 180) * latitude     # convert to radian
    r_earth = getRadiusofEarth(lat_rad) # radius of earth at given latitude
    # r_earth = 6371.001    # average radius of earth (in km)
    r_earth *= 1000       # in metres
    return (resolution * 360) / (2 * r_earth * math.pi)

      

def genMatrix(lat1, lon1, lat2, lon2, res):
    '''generate matrix of coordinates using corner points'''
    result = []
    lat_diff = abs(changeInLatitude(res, lat1))
    lon_diff = abs(changeInLongitude(res, lat1))

    start_lat = max(lat1, lat2)
    start_lon = min(lon1, lon2)
    end_lat = min(lat1, lat2)
    end_lon = max(lon1, lon2)

    lat1, lon1 = start_lat, start_lon
    lat2, lon2 = end_lat, end_lon

    print("start: ", start_lat, start_lon)
    print("end: ", end_lat, end_lon)
    
    # if (lat1 < lat2 and lon1 < lon2):
    #     start_lat = lat2
    #     start_lon = lon1
    #     end_lat = lat1
    #     end_lon = lon2
    # if (lat1 > lat2 and lon1 < lon2):
    #     start_lat = lat1
    #     start_lon = lon1
    #     end_lat = lat2
    #     end_lon = lon2
    # elif (lat1 < lat2 and lon1 > lon2):
    #     start_lat = lat2
    #     start_lon = lon2
    #     end_lat = lat1
    #     end_lon = lon1
    # elif (lat1 > lat2 and lon1 > lon2):
    #     start_lat = lat1
    #     start_lon = lon2
    #     end_lat = lat2
    #     end_lon = lon1

    while (start_lat > end_lat):
        row = []
        temp_lon = start_lon
        while (temp_lon <= end_lon):
            row.append([start_lat, temp_lon])
            temp_lon += lon_diff
        start_lat -= lat_diff
        result.append(row)
    print("shape: ", len(result), len(result[0]))
    return result  
    
def distanceBetwenPoints(lat1, lat2, lon1, lon2):
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    # calculate the result
    return(c * r)


def findIndex(lat_input, lon_input, lat1, lon1, lat2, lon2, res):
    lat_zero = max(lat1, lat2)
    lon_zero = min(lon1, lon2)
    latIndex = (lat_zero - lat_input) // abs(changeInLatitude(res, lat_zero))
    lonIndex = (lon_input - lon_zero) // abs(changeInLongitude(res, lat_zero))
    return int(latIndex), int(lonIndex)


def neighbourDist(x1, y1, x2, y2, res):
    # Non Diagonal points
    if((abs(x1-x2)==1 and abs(y1-y2)==0) or (abs(x1-x2)==0 and abs(y1-y2)==1)):
        return res
    # Diagnoal points
    elif(abs(x1-x2)==1 and abs(y1-y2)==1):
        return res * (2**0.5)
    

def euclideanDist(elevation_map, x1, y1, x2, y2, h_weight, res):
    hor_dist = (((x1 - x2)**2 + (y1 - y2)**2)**0.5 )*res
    vert_dist = elevation_map[x1][y1] - elevation_map[x2][y2]
    return ((hor_dist*h_weight)**2 + vert_dist**2)**0.5