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

    def send(self, message):
        self._pipe_in.send(message)

    def receive(self):
        return self._pipe_out.recv()

    def _run(self):
        self.init()
        while True:
            self.loop()

class Application(Process):
    def init(self):
        broker = Broker()
        self._library = Library(broker)
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
    def __init__(self, broker):
        self._broker = broker
        self._books = []
        self._authors = []

    def add(self, book):
        self._books.append(book)
        if not book.author in self._authors:
            self.add_author(book.author)
        self._broker.send(BookAddedEvent(book.name, book.author))

    def add_author(self, author):
        self._authors.append(author)
        self._broker.send(AuthorAddedEvent(author))

class Book:
    def __init__(self, name, author):
        self.name = name
        self.author = author

class BookAddedEvent:
    def __init__(self, name, author):
        pass

class AuthorAddedEvent:
    def __init__(self, name):
        pass

class Broker:
    def __init__(self):
        self._listeners = []
    def send(self, event):
        [l.send(event) for l in self._listeners]
    def add_listener(self, l):
        self._listeners.append(l)
