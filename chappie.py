#!/usr/bin/env python
import sys
import cv2
from chappieEyes import Eyes
from chappieHead import Head
from chappieBrain import Brain

performance = 0


def print_help():
    print ""
    print "e - eyes postprocessing"
    print "h - head moves on/off"
    print "b - brain mode"
    print "p - performance measurement"
    print "? - help"
    print "q - quit"

# initialize
eyes = Eyes(int(sys.argv[1]))
head = Head(sys.argv[2], 0)
brain = Brain(eyes, head)
print_help()

while True:
    t1 = cv2.getTickCount()

    # read senses
    frame = eyes.look()

    t2 = cv2.getTickCount()

    # process data
    brain.attention(frame)

    # measure performance
    if performance > 0:
        t3 = cv2.getTickCount()
        te = (t2-t1)/cv2.getTickFrequency()
        tb = (t3-t2)/cv2.getTickFrequency()
        fps = cv2.getTickFrequency()/(t3-t1)
        print ("\re: %f b: %f fps: %f" % (te, tb, fps)),

    # control center
    k = cv2.waitKey(1) & 0xFF
    if k == ord('e'):
        eyes.set_cfg()
    elif k == ord('h'):
        head.set_cfg()
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
eyes.close()
cv2.destroyAllWindows()
