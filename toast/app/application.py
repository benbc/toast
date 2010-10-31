class Process:
    def start(self):
        import multiprocessing
        (self._pipe_out, self._pipe_in) = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=self.init)
        p.start()

    def send(self, command):
        self._pipe_in.send(command)

    def receive(self):
        return self._pipe_out.recv()

    def init(self):
        while True:
            self.loop()

class Application(Process):
    def loop(self):
        command = self.receive()
        print("In app: %s" % command)
        self.persist(command)
        self.execute(command)

    def persist(self, command):
        pass

    def execute(self, command):
        pass
