import requests as rq
import json



def elevationApiResponse(pointsObj,apiEndPoint):
    # apiEndPoint = "http://localhost/api/v1/lookup"
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = rq.post(apiEndPoint, data=json.dumps(pointsObj), headers=header)
    # return response
    jsonResult = response.json()
    return jsonResult['results'] # n*m  

locationDict = {
    "locations":
	[
		{
			"latitude": -109.83007049344715, 
			"longitude": 44.36470033197011
		}
		# {
		# 	"latitude": 32.720726,
		# 	"longitude": 76.069866
		# },
		# {
		# 	"latitude":41.161758,
		# 	"longitude":-8.583933
		# }
	]}

# 77.43407308022033,31.58360498413924

coord = {
    'latitude': 31.58360498413924,
    'longitude': 77.43407308022033}
# locationDict['locations'].append(coord)

apiEndPoint = "http://localhost/api/v1/lookup"
print(elevationApiResponse(locationDict,apiEndPoint))
# apiEndPoint = "https://api.open-elevation.com//api/v1/lookup"
# print(elevationApiResponse(locationDict,apiEndPoint))
# 'https://api.open-elevation.com/api/v1/lookup?locations=10,10|20,20|41.161758,-8.583933'
# apiEndPoint = "http://localhost:8080/api/v1/lookup"




# apiEndPoint = 'http://localhost/api/v1/lookup?locations= 31.5836,77.4340'
# response = rq.get(apiEndPoint)
# if response.status_code==200:
#     print(response.json())
# else:
#     print(response.status_code)