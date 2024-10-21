#!/usr/bin/env python3
from __future__ import print_function
import requests
import json
import time
import sys
import base64
import jsonpickle
import random

def doRawImage(addr, debug=False):
    # prepare headers for http request
    headers = {'content-type': 'image/png'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    # send http request with image and receive response
    image_url = addr + '/api/rawimage'
    response = requests.post(image_url, data=img, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doAdd(addr, debug=False):
    headers = {'content-type': 'application/json'}
    # send http request with image and receive response
    add_url = addr + "/api/add/5/10"
    response = requests.post(add_url, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doDotProduct(addr, debug=False):
    # REST params
    headers = {'content-type': 'application/json'}
    dot_product_url = addr + "/api/dotproduct"

    # generate 100 random numbers
    random.seed(42)
    n = 100
    a = [random.random() for _ in range(n)]
    b = [random.random() for _ in range(n)]
   
    # send POST request
    payload = {'a': a, 'b': b }
    response = requests.post(dot_product_url, data=json.dumps(payload), headers=headers)
    
    if debug:
        print("Response is", response)
        print(response.json().get('result'))

def doJsonImage(addr, debug=False):
    # REST params
    headers = {'content-type': 'application/json'}
    json_img_url = addr + "/api/jsonimage"

    # open and encode image
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    encoded_img = base64.b64encode(img).decode('utf-8')

    # send POST request
    payload = {'image': encoded_img}
    response = requests.post(json_img_url, data=json.dumps(payload), headers=headers)
    
    if debug:
        print("Response is")
        print(response.json())

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, sum or jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"http://{host}:5050"
print(f"Running {reps} reps against {addr}")

debug_mode = False

if cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage(addr, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd(addr, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage(addr, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct(addr, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)