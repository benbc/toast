import multiprocessing

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
