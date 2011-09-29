import json
from model import Book

class AddRecipeCommand(object):
    def __init__(self, book_id, title):
        self._data = {'book_id': book_id, 'title': title}
    def __str__(self):
        return "%s/%s" % (self._data['book_id'],
                          self._data['title'])
    def execute(self, library, broker):
        book = library.find_book(self._data['book_id'])
        book.add_recipe(self._data['title'])

class AddBookCommand(object):
    def __init__(self, name, author):
        self._data = {'name': name, 'author': author}
    def __str__(self):
        return "%s - %s" % (self._data['name'],
                            self._data['author'])
    def execute(self, library, broker):
        library.add(Book(broker, self._data['name'],
                         self._data['author']))

def serialize(command):
    record = {'name': type(command).__name__,
              'data': command._data}
    return json.dumps(record)

def deserialize(string):
    record = json.loads(string)
    klass = globals()[record['name']]
    command = klass.__call__(**record['data'])
    return command
