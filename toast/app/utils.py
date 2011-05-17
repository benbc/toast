class Ids:
    def __init__(self):
        self._next_id = 0;
    def next(self):
        id = self._next_id
        self._next_id += 1
        return id
