"""The Python implementation of the GRPC helloworld.Greeter server."""

import time

import greeting_pb2 as helloworld_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2.BetaGreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
  server = helloworld_pb2.beta_create_Greeter_server(Greeter())
  server.add_insecure_port('[::]:50051')
  server.start()
  print 'Server started'
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
