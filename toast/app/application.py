from model import Library
from database import Database
from process import Process
from commands import serialize, deserialize

class Application(Process):
    def __init__(self):
        Process.__init__(self, 'application')
        self._broker = Broker()
        self._library = Library(self._broker)

    def initialize(self):
        self._replay()

    def add_listener(self, listener):
        self._broker.add_listener(listener)

    def loop(self):
        command = self.receive()
        self._persist(command)
        self._execute(command)

    def _replay(self):
        with open('log/command.log', 'r') as f:
            for line in f:
                command = deserialize(line)
                self._execute(command)

    def _persist(self, command):
        with open('log/command.log', 'a') as f:
            f.write(serialize(command))

    def _execute(self, command):
        print("application executing: %s" % command)
        command.execute(self._library, self._broker)

class Broker:
    def __init__(self):
        self._listeners = []
    def send(self, event):
        [l.send(event) for l in self._listeners]
    def add_listener(self, l):
        self._listeners.append(l)

def build_application():
    database = Database()
    application = Application()
    application.add_listener(database)
    database.start()
    application.start()

    return (application, database)
