class Mouth(object):
    p = None
    stream = None

    def __init__(self, ears):
        self.p = ears.p
        self.stream = self.p.open(output=True, channels=ears.channels, rate=ears.rate, format=ears.format)
        return

    def talk(self, record):
        self.stream.write(record)
        return

    def close(self):
        self.stream.close()
        return
