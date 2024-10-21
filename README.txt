Speed Comparison of REST and gRPC
---------------------------------

The below table records the average time taken for response when the server is hosted in different machines at different locations for REST and gRPC implementation of different functions. There are four different functions:

1. add - receives two integers and computes the sum
2. rawimg - receives a 2d image as bytes and computes it's width and height
3. dotProduct - computes the dot product of two given arrays
4. jsonimg - same as rawimg, but the image is encoded and transmitted instead of being shared raw.
5. ping - round trip time taken for a packet to reach the server.


|  Method 	        | Local  	| Same-Zone  	|  Different Region 	|
|-------------------|-----------|---------------|-----------------------|
|   REST add	    | 2.6ms	    | 3.015ms       | 296.68ms              |
|   gRPC add	    | 0.77ms    | 0.90ms        | 143.92ms              |
|   REST rawimg	    | 4.88ms  	| 7.33ms        | 1200ms                |
|   gRPC rawimg	    | 9.89ms    | 11.45ms       | 196.50ms              |
|   REST dotproduct	| 2.96ms  	| 3.45ms        | 297.49ms             	|
|   gRPC dotproduct	| 0.96ms    | 1.06ms        | 143.92ms             	|
|   REST jsonimg	| 38.02ms  	| 40.84ms       | 1341.86ms             |
|   gRPC jsonimg	| 26.25ms   | 29.12ms       | 229.65ms              |
|   PING            | 0.033ms   | 0.257ms       | 142ms                 |


The ping row represents time taken for just one packet to reach the server and come back. It can be used as a baseline time that will be taken for the packet to travel over a network.

From the timings, it is discernible that gRPC consistently outperforms REST in all scenarios—local, same-zone, and different region. In all the scenarios for add operation, we can see that the gRPC implementation's average time taken is closer to the PING time, but it is not the case for REST. This can be attributed to multiple reasons. One the size of the serialized data is larger for JSON compared to the data serialized using Protocol Buffers.

Network latency also plays an important role. REST uses http1.1 which has a more basic compression compared to http 2 which is used by gRPC. gRPC also supports bidirectional streaming in which a single connection will be enough for the packets to go and come back. REST does not support this, hence multiple connections have to be established. This is particularly visible in the implementation involving different region, where the time taken for the response is closer to PING time in gRPC implementation, whereas it is almost double the size in REST implementation.

Suprisingly, passing rawImage over gRPC in a local host implementation and same zone is slower when compared to that of REST. But when the distance gets higher, gRPC again proves to be faster than REST.

The overhead of REST's connection setup compounds the delays, making gRPC a much better choice for high-latency or high-throughput scenarios.