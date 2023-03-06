import ee
# ee.Authenticate()
ee.Authenticate()
# Initialize the library.
ee.Initialize()
# print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
dataset = ee.ImageCollection("ESA/WorldCover/v100");
gem=ee.Geometry.Point([76.93418072406776,31.715261419014443])
selectedIm = dataset.filterBounds(gem)
print(selectedIm)


# apikey="AIzaSyD71g5TRbdsmGWa4nrxWUdKfe_MKy8E9MY"
# import requests

# url = f"https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536%2C-104.9847034&key={apikey}"

# payload={}
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)