import greeting_pb2 as helloworld_pb2
from grpc.beta import implementations
from gevent import monkey

monkey.patch_all(thread=False)

channel = implementations.insecure_channel('localhost', 50051)
print("Creating Greeter client...")
stub = helloworld_pb2.beta_create_Greeter_stub(channel)
print("Greeter client created!")
response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'), 10)
print "Greeter client received: " + response.message
del stub

