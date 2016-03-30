import threading
import cv2
from chappie import chappie
from chappieSound import chappie_sound


class ChappieThread(threading.Thread):

    def run(self):
        chappie()
        return


class ChappieSoundThread(threading.Thread):

    def run(self):
        chappie_sound()
        return


if __name__ == '__main__':
    chappie_thread = ChappieThread()
    chappie_sound_thread = ChappieSoundThread()
    chappie_thread.start()
    chappie_sound_thread.start()
    chappie_thread.join()
    chappie_sound_thread.join()
    cv2.destroyAllWindows()
