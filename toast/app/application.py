import multiprocessing
import pickle

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
        command.execute(self._library, self._ids)

class Ids:
    def __init__(self):
        self._next_id = 0;
    def next(self):
        id = self._next_id
        self._next_id += 1
        return id

class Library:
    def __init__(self, broker):
        self._broker = broker
        self._books = []
        self._authors = AuthorList(broker)

    def add(self, book):
        self._books.append(book)
        book.add_author_to(self._authors)
        self._broker.send(book.write_to(BookAddedEvent))

class AuthorList:
    def __init__(self, broker):
        self._authors = []
        self._broker = broker
    def add(self, author):
        if not author in self._authors:
            self._authors.append(author)
            self._broker.send(AuthorAddedEvent(author))

class Book:
    def __init__(self, ids, name, author):
        self._id = ids.next()
        self._name = name
        self._author = author
    def write_to(self, target):
        return target(self._id, self._name, self._author)
    def add_author_to(self, authors):
        authors.add(self._author)

class BookAddedEvent:
    def __init__(self, id, name, author):
        self._id = id
        self._name = name
        self._author = author
    def accept(self, visitor):
        visitor.handle_book_added(self._id, self._name, self._author)
    def __str__(self):
        return "BookAddedEvent(%s, %s)" % (self._name, self._author)

class AuthorAddedEvent:
    def __init__(self, name):
        self._name = name
    def accept(self, visitor):
        visitor.handle_author_added(self._name)
    def __str__(self):
        return "AuthorAddedEvent(%s)" % (self._name)

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
        self._data['books'] = []

    def loop(self):
        event = self.receive()
        self._handle(event)

    def _handle(self, event):
        print("database handling: %s" % event)
        event.accept(self)

    def handle_book_added(self, id, name, author):
        books = self._data['books']
        books.append({'id': id, 'name': name, 'author': author, 'recipes': []})
        self._data['books'] = books

    def handle_author_added(self, name):
        authors = self._data['authors']
        authors.append(name)
        self._data['authors'] = authors

    def books(self):
        return self._data['books']
    def book(self, id):
        return [b for b in self.books() if b['id']==id][0]
    def authors(self):
        return self._data['authors']

def build_application():
    database = Database()
    application = Application()
    application.add_listener(database)

    database.start()
    application.start()

    return (application, database)
