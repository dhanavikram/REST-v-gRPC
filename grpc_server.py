#!/usr/bin/env python3
import grpc
import io
from PIL import Image
import base64
from concurrent import futures
import grpc_pb2
import grpc_pb2_grpc

class AddTwoNums(grpc_pb2_grpc.addServicer):
    def addTwoNumbers(self, request, context):
        result = request.a + request.b
        return grpc_pb2.addReply(sum = result)

class RawImage(grpc_pb2_grpc.rawImageServicer):
    def computeImage(self, request, context):
        ioBuffer = io.BytesIO(request.img)
        img = Image.open(ioBuffer)
        return grpc_pb2.imageReply(width=img.size[0], height=img.size[1])

class DotProduct(grpc_pb2_grpc.dotProductServicer):
    def computeDotProduct(self, request, context):
        a = request.a
        b = request.b
        result = sum(i[0]*i[1] for i in zip(a, b))
        return grpc_pb2.dotProductReply(dotproduct=result)
    
class JsonImage(grpc_pb2_grpc.jsonImageServicer):
    def computeJsonImage(self, request, context):
        img = request.img
        decoded_image = base64.b64decode(img)
        # find size of the image
        image = Image.open(io.BytesIO(decoded_image))
        return grpc_pb2.imageReply(width=image.size[0], height=image.size[1])

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_addServicer_to_server(AddTwoNums(), server)
    grpc_pb2_grpc.add_rawImageServicer_to_server(RawImage(), server)
    grpc_pb2_grpc.add_dotProductServicer_to_server(DotProduct(), server)
    grpc_pb2_grpc.add_jsonImageServicer_to_server(JsonImage(), server)
    server.add_insecure_port('[::]:5050')
    server.start()
    print("GRPC Server started on port 5050")
    server.wait_for_termination()