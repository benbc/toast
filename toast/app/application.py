import pickle

class Process:
    def start(self):
        import multiprocessing
        (self._pipe_out, self._pipe_in) = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=self._run)
        p.start()

    def init(self):
        """Override if the process needs initialization."""
        pass

    def send(self, command):
        self._pipe_in.send(command)

    def receive(self):
        return self._pipe_out.recv()

    def _run(self):
        self.init()
        while True:
            self.loop()

class Application(Process):
    def init(self):
        self._library = Library()
        self._replay()

    def loop(self):
        command = self.receive()
        self._persist(command)
        self._execute(command)

    def _replay(self):
        with open('log/command.log', 'r') as f:
            try:
                while True:
                    command = pickle.load(f)
                    self._execute(command)
            except EOFError:
                pass

    def _persist(self, command):
        with open('log/command.log', 'a') as f:
            pickle.dump(command, f)

    def _execute(self, command):
        print("executing %s" % command)
        command.execute(self._library)

class Library:
    def __init__(self):
        self._books = []
    def add(self, book):
        self._books.append(book)

class Book:
    def __init__(self, name, author):
        pass
