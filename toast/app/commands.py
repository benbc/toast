from model import Book

class AddRecipeCommand:
    def __init__(self, book_id, title):
        self._book_id = book_id
        self._title = title
    def __str__(self):
        return "%s/%s" % (self._book_id, self._title)
    def execute(self, library, broker):
        book = library.find_book(self._book_id)
        book.add_recipe(self._title)

class AddBookCommand:
    def __init__(self, name, author):
        self.name = name
        self.author = author
    def __str__(self):
        return "%s - %s" % (self.name, self.author)
    def execute(self, library, broker):
        library.add(Book(broker, self.name, self.author))
