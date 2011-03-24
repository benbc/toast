import multiprocessing
import pickle
from model import Library, Ids

class Process:
    def start(self):
        (self._pipe_out, self._pipe_in) = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=self._run)
        p.start()

    def initialize(self):
        """Override if the process needs initialization."""
        pass

    def send(self, message):
        self._pipe_in.send(message)

    def receive(self):
        return self._pipe_out.recv()

    def _run(self):
        self.initialize()
        while True:
            self.loop()

class Application(Process):
    def __init__(self):
        self._broker = Broker()
        self._library = Library(self._broker)
        self._ids = Ids()

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
        print("application executing: %s" % command)
        command.execute(self._library, self._ids, self._broker)

class Broker:
    def __init__(self):
        self._listeners = []
    def send(self, event):
        [l.send(event) for l in self._listeners]
    def add_listener(self, l):
        self._listeners.append(l)

class Database(Process):
    def __init__(self):
        self._data = multiprocessing.Manager().dict()
        self._data['authors'] = []
        self._data['books'] = {}

    def loop(self):
        event = self.receive()
        self._handle(event)

    def _handle(self, event):
        print("database handling: %s" % event)
        event.accept(self)

    def handle_book_added(self, id, name, author):
        self._modifying_books(lambda books: books.__setitem__(id, {'id': id, 'name': name, 'author': author, 'recipes': []}))

    def handle_author_added(self, name):
        authors = self._data['authors']
        authors.append(name)
        self._data['authors'] = authors

    def handle_recipe_added(self, book_id, name):
        self._modifying_books(lambda books: books[book_id]['recipes'].append(name))

    def books(self):
        return self._data['books'].values()
    def book(self, id):
        return self._data['books'][id]
    def authors(self):
        return self._data['authors']

    def _modifying_books(self, f):
        books = self._data['books']
        f(books)
        self._data['books'] = books

def build_application():
    database = Database()
    application = Application()
    application.add_listener(database)

    database.start()
    application.start()

    return (application, database)
