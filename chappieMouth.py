import threading


class MouthThread(threading.Thread):
    stream = None
    record = None

    def __init__(self, stream, record):
        self.stream = stream
        self.record = record
        super(MouthThread, self).__init__()
        return

    def run(self):
        self.stream.write(self.record)
        return


class Mouth(object):
    p = None
    stream = None
    thread = None

    def __init__(self, ears):
        self.p = ears.p
        self.stream = self.p.open(output=True, channels=ears.channels, rate=ears.rate, format=ears.format)
        # rate=22000 for squirrels
        return

    def talk(self, record):
        if self.thread is not None:
            self.thread.join()
        self.thread = MouthThread(self.stream, record)
        self.thread.start()
        return

    def close(self):
        self.stream.close()
        return

    def is_speaking(self):
        if self.thread is not None:
            return self.thread.is_alive()
        else:
            return False
