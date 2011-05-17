import multiprocessing
import zmq
from utils import Ids

class Process:
    _ids = Ids()

    def __init__(self, name):
        self._name = name
        id = Process._ids.next()
        self._message_port = 5100 + id
        self._control_port = 5000 + id

    def start(self):
        p = multiprocessing.Process(target=self._run)
        p.start()
        self._wait_for_ready()

    def initialize(self):
        """Override if the process needs initialization."""
        pass

    def send(self, message):
        context = zmq.Context()
        connection = context.socket(zmq.PUB)
        connection.connect('tcp://localhost:%s' % self._message_port)
        connection.send_pyobj(message)

    def receive(self):
        return self._connection.recv_pyobj()

    def _run(self):
        self._context = zmq.Context()
        self._connection = self._context.socket(zmq.SUB)
        self._connection.bind('tcp://*:%s' % self._message_port)
        self._connection.setsockopt(zmq.SUBSCRIBE, '')
        self.initialize()
        self._signal_ready()
        while True:
            self.loop()

    def _wait_for_ready(self):
        context = zmq.Context()
        control_socket = context.socket(zmq.PAIR)
        control_socket.bind('tcp://*:%s' % self._control_port)
        control_socket.recv()

    def _signal_ready(self):
        control_socket = self._context.socket(zmq.PAIR)
        control_socket.connect('tcp://localhost:%s' % self._control_port)
        control_socket.send('ready')
