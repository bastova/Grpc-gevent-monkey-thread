import greeting_pb2 as helloworld_pb2
from grpc.beta import implementations
from gevent import monkey
import concurrent.futures
from gevent.threadpool import ThreadPool

class ThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
  """
  A version of :class:`concurrent.futures.ThreadPoolExecutor` that
  always uses native threads, even when threading is monkey-patched.

  TODO: Gevent has also implemented [ThreadPoolExecutor](https://github.com/gevent/gevent/blob/master/src/gevent/threadpool.py#L454)
   to be released in next version 1.2.0. We should move to that implementation when it is released.
  """

  def __init__(self, max_workers):
    super(ThreadPoolExecutor, self).__init__(max_workers)
    self._threadpool = ThreadPool(max_workers)

  def submit(self, fn, *args, **kwargs):
    future = super(ThreadPoolExecutor, self).submit(fn, *args, **kwargs)
    with self._shutdown_lock:
      work_item = self._work_queue.get()
      assert work_item.fn is fn

    self._threadpool.spawn(work_item.run)
    return future

  def shutdown(self, wait=True):
    super(ThreadPoolExecutor, self).shutdown(wait)
    self._threadpool.kill()

  kill = shutdown  # greentest compat

  def _adjust_thread_count(self):
    # Does nothing. We don't want to spawn any "threads",
    # let the threadpool handle that.
    pass

monkey.patch_all()

concurrent.futures.ThreadPoolExecutor = ThreadPoolExecutor

channel = implementations.insecure_channel('localhost', 50051)
print("Creating Greater client (w/ gevent patched ThreadPoolExecutor); the calls to the server fail with 'This operation would block forever' :\(")
stub = helloworld_pb2.beta_create_Greeter_stub(channel)
print("Greeter client created!") 
response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'), 10)
print "Greeter client received: " + response.message
del stub

