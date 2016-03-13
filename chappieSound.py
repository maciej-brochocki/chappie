#!/usr/bin/env python
import cv2
from chappieEars import Ears
from chappieMouth import Mouth
from chappieSoundBrain import Brain
import pyaudio

performance = 0


def print_help():
    print ""
    print "- - silence threshold down"
    print "+ - silence threshold up"
    print "b - brain mode"
    print "p - performance measurement"
    print "? - help"
    print "q - quit"

# initialize
p = pyaudio.PyAudio()
ears = Ears(p)
mouth = Mouth(ears)
brain = Brain(ears, mouth)
print_help()

while True:
    t1 = cv2.getTickCount()

    # read senses
    sound = ears.hear()

    t2 = cv2.getTickCount()

    # process data
    brain.attention(sound)

    # measure performance
    if performance > 0:
        t3 = cv2.getTickCount()
        te = (t2-t1)/cv2.getTickFrequency()
        tb = (t3-t2)/cv2.getTickFrequency()
        fps = cv2.getTickFrequency()/(t3-t1)
        print ("\re: %f b: %f fps: %f" % (te, tb, fps)),

    # control center
    k = cv2.waitKey(1) & 0xFF
    if k == ord('-'):
        brain.dec_silence_threshold()
    elif k == ord('+'):
        brain.inc_silence_threshold()
    elif k == ord('b'):
        brain.set_cfg()
    elif k == ord('p'):
        performance = 1 - performance
        if performance == 0:
            print ""
    elif k == ord('?'):
        print_help()
    elif k == ord('q'):
        break

# clean up
ears.close()
mouth.close()
cv2.destroyAllWindows()
p.terminate()
