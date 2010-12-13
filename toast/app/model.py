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
