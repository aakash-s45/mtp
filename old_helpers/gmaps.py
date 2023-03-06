# import googlemaps
# from datetime import datetime

# gmaps = googlemaps.Client(key='AIzaSyDdCfOVD62Ym1GI603WSk0QrB0u1bUEviE')

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

import requests

url = "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536%2C-104.9847034&key=AIzaSyDdCfOVD62Ym1GI603WSk0QrB0u1bUEviE"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)