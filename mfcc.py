import numpy as np


class Mfcc(object):
    a = None

    def encode(self, sound):
        self.a = np.fromstring(sound, dtype=np.uint16)
        return
