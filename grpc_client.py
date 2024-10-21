#!/usr/bin/env python3
from __future__ import print_function
import time
import sys
import base64
import random
import grpc
import grpc_pb2
import grpc_pb2_grpc

def doAdd(channel, debug = False):
    stub = grpc_pb2_grpc.addStub(channel)
    response = stub.addTwoNumbers(grpc_pb2.addMsg(a=5, b=3))
    
    if debug:
       print(f"The sum is: {response.sum}") 

def doRawImage(channel, debug = False):
    stub = grpc_pb2_grpc.rawImageStub(channel)
    
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    response = stub.computeImage(grpc_pb2.rawImageMsg(img=img))
    
    if debug:
        print(f"Width: {response.width} and Height: {response.height}")

def doDotProduct(channel, debug = False):
    stub = grpc_pb2_grpc.dotProductStub(channel)
    
    # generate 100 random numbers
    random.seed(42)
    n = 100
    a = [random.random() for _ in range(n)]
    b = [random.random() for _ in range(n)]
    
    data = grpc_pb2.dotProductMsg(a=a, b=b)
    response = stub.computeDotProduct(data)
    
    if debug:
        result = sum(i[0]*i[1] for i in zip(a, b))
        print(result)
        print(f"The sum is: {response.dotproduct}")

def doJsonImage(channel, debug = False):
    stub = grpc_pb2_grpc.jsonImageStub(channel)

    # open and encode image
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    encoded_img = base64.b64encode(img).decode('utf-8')

    data = grpc_pb2.jsonImageMsg(img=encoded_img)
    response = stub.computeJsonImage(data)

    if debug:
        print(f"Width: {response.width} and Height: {response.height}")


if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, sum or jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

channel = grpc.insecure_channel(f'{host}:5050')
print(f"Running {reps} reps")

debug_mode = True

if cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage(channel, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd(channel, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage(channel, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif cmd == 'dotProduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct(channel, debug=debug_mode)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

else:
    print("Unknown option", cmd)