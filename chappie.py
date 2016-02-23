#!/usr/bin/env python
import sys
import cv2
from chappieEyes import Eyes
from chappieHead import Head
from chappieBrain import Brain

# initialize
eyes = Eyes(int(sys.argv[1]))
head = Head(sys.argv[3], 1)
brain = Brain(eyes, head, sys.argv[2])

while True:
    t1 = cv2.getTickCount()

    # read senses
    frame = eyes.look()

    t2 = cv2.getTickCount()

    # process data
    brain.attention(frame)

    # measure performance
    t3 = cv2.getTickCount()
    te = (t2-t1)/cv2.getTickFrequency()
    tb = (t3-t2)/cv2.getTickFrequency()
    fps = cv2.getTickFrequency()/(t3-t1)
    print "e: %f b: %f fps: %f" % (te, tb, fps)

    # control center
    k = cv2.waitKey(1) & 0xFF
    if k == ord('1'):
        eyes.setCfg(1)
    elif k == ord('2'):
        eyes.setCfg(2)
    elif k == ord('3'):
        eyes.setCfg(3)
    elif k == ord('4'):
        head.setCfg(0)
    elif k == ord('5'):
        head.setCfg(1)
    elif k == ord('6'):
        brain.setCfg(1)
    elif k == ord('7'):
        brain.setCfg(2)
    elif k == ord('q'):
        break

#clean up
eyes.close()
brain.sleep()

