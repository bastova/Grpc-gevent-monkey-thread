gRPC + gevent monkey patch tests
==========================

Prerequisite:
------------

- docker


How to run sample?
------------------

###### First start the grpc server 

`$ ./run_greeter_server.sh`

###### To run grpc sample code with gevent monkey patching and overriding ThreadPoolExecutor

`$ ./run_greeter_with_patched_threadpoolexecutor.sh`

This will build and run docker container that executes [greeter_client_with_patched_threadpoolexecutor.py](https://github.com/bastova/Grpc-gevent-mokey-thread/blob/master/greeter_client_with_patched_threadpoolexecutor.py).
As of current gRPC implementation (grpcio==0.13.0), it will result in 'This operation would block forever' exception from Grpc (core). Press `<ctrl+c>` to exit docker term and then `docker rm -f greeter_with_patch` to kill and remove the container.



###### To run grpc sample code with gevent monkey patching but __without__ patching thread.

`$ ./run_greeter_with_unpatched_thread.sh`

This will build and run docker container that executes [greeter_client_with_unpatched_thread.py](https://github.com/bastova/Grpc-gevent-mokey-thread/blob/master/greeter_client_with_unpatched_thread.py)
It will execute successfully and or finish with a Timeout (expected behavior if sockets refuse connection to server).

