import multiprocessing
from process import Process

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
