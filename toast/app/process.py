import multiprocessing
import zmq
from utils import Ids

class Process:
    _ids = Ids()

    def __init__(self, name):
        self._name = name
        self._port = 5100 + Process._ids.next()

    def start(self):
        p = multiprocessing.Process(target=self._run)
        p.start()

    def initialize(self):
        """Override if the process needs initialization."""
        pass

    def send(self, message):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect('tcp://localhost:%s' % self._port)
        socket.send_pyobj(message)

    def receive(self):
        return self._socket.recv_pyobj()

    def _run(self):
        self._connect()
        self.initialize()
        while True:
            self.loop()

    def _connect(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.PULL)
        self._socket.bind('tcp://*:%s' % self._port)
