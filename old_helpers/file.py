import requests as rq
import json

# print("Using GET")
# response = rq.get('https://api.open-elevation.com/api/v1/lookup?locations=10,10|20,20|41.161758,-8.583933')
# response = rq.get('http://localhost/api/v1/lookup?locations=33,77|34,77')
# print(f"Status :{response.status_code}")
# print(response.json())




print()
print("Using POST")

myobj = {"locations":
            [
                {
                    "latitude": 33,
                    "longitude": 77
                },
                {
                    "latitude": 20,
                    "longitude": 20
                },
                {
                    "latitude": 41.161758,
                    "longitude": -8.583933
                }
            ]
        }

header = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# apiEndPoint = "https://api.open-elevation.com/api/v1/lookup"
apiEndPoint = "http://localhost/api/v1/lookup"

# # using POST
response = rq.post(apiEndPoint, data=json.dumps(myobj), headers=header)

print(f"Status :{response.status_code}")
jsonResult = response.json()
listOfPoints = jsonResult['results']

for point in listOfPoints:
    print("-----------------")
    print(f"Latitude: {point['latitude']}")
    print(f"Longitude: {point['longitude']}")
    print(f"Elevation: {point['elevation']}")
