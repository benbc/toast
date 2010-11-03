class Process:
    def start(self):
        import multiprocessing
        (self._pipe_out, self._pipe_in) = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=self.run)
        p.start()

    def send(self, command):
        self._pipe_in.send(command)

    def receive(self):
        return self._pipe_out.recv()

    def run(self):
        self.init()
        while True:
            self.loop()

    def init(self):
        """Override if the process needs initialization."""
        pass

class Application(Process):
    def init(self):
        self.replay()

    def loop(self):
        command = self.receive()
        print("In app: %s" % command)
        self.persist(command)
        self.execute(command)

    def replay(self):
        pass

    def persist(self, command):
        pass

    def execute(self, command):
        pass
