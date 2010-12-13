from application import Book

class AddLineCommand:
    def __init__(self, line):
        self._line = line
    def __str__(self):
        return self._line
    def execute(self, library, ids):
        pass

class AddBookCommand:
    def __init__(self, name, author):
        self.name = name
        self.author = author
    def __str__(self):
        return "%s - %s" % (self.name, self.author)
    def execute(self, library, ids):
        library.add(Book(ids, self.name, self.author))
