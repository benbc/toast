class Library:
    def __init__(self, broker):
        self._broker = broker
        self._books = []
        self._authors = AuthorList(broker)

    def add(self, book):
        self._books.append(book)
        book.add_author_to(self._authors)
        self._broker.send(book.write_to(BookAddedEvent))

    def find_book(self, id):
        for b in self._books:
            if b.has_id(id):
                return b

class AuthorList:
    def __init__(self, broker):
        self._authors = []
        self._broker = broker
    def add(self, author):
        if not author in self._authors:
            self._authors.append(author)
            self._broker.send(AuthorAddedEvent(author))

class Book:
    def __init__(self, broker, name, author):
        self._broker = broker
        self._name = name
        self._author = author
        self._recipes = []
        self._id = abs(hash("%s/%s" % (name, author)))
    def write_to(self, target):
        return target(self._id, self._name, self._author)
    def add_author_to(self, authors):
        authors.add(self._author)
    def add_recipe(self, title):
        self._broker.send(RecipeAddedEvent(self._id, title))
        self._recipes.append(Recipe(title))
    def has_id(self, id):
        return self._id == id

class Recipe:
    def __init__(self, title):
        self._title = title

class RecipeAddedEvent:
    def __init__(self, book_id, recipe):
        self._book_id = book_id
        self._recipe = recipe
    def accept(self, visitor):
        visitor.handle_recipe_added(self._book_id, self._recipe)
    def __str__(self):
        return "RecipeAddedEvent(%s, %s)" % (self._book_id, self._recipe)

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
