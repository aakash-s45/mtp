import requests as rq
import json
import threading
from threading import Thread
from time import sleep 

def func(variable, val):
      variable.append([0,val])
      print(f'variable {val} set to value: {variable}')


def multithread():
	MAX_THREAD = 4
    # creating list of size MAX_THREAD
	thread = list(range(MAX_THREAD))
    # creating MAX_THEAD number of threads
	variable = [[0,0], [0,1]]
	values = [0, 1, 2, 3]
	for i in range(MAX_THREAD):
		thread[i] = Thread(target=func, args=(variable, values[i]))
		thread[i].start()
                
    # Waiting for all threads to finish
	for i in range(MAX_THREAD):
		thread[i].join()

	print(f'variable final value is {variable}')

# multithread()


class foo:
    x = 0
    
def increase(foo):
    for i in range(3):
        print(f"[{threading.currentThread().getName()}] X is {foo.x}")
        foo.x += 1
        print(f"[{threading.currentThread().getName()}] X is now {foo.x} after increase")
        sleep(0.5)
        print(f"[{threading.currentThread().getName()}] X is now {foo.x} after sleep")
    return foo.x 

def testing():
    x = foo() 
    first = threading.Thread(name="Thread One", target=increase,args=([x]))
    second = threading.Thread(name="Thread Two", target=increase,args=([x]))
    
    first.start()
    second.start()
    
    first.join()
    second.join()  
    print(x.x)

# testing()






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


def main():
	locationDict = {
		"locations":
		[
			{
				"latitude": -109.83007049344715, 
				"longitude": 44.36470033197011
			}
		]}
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