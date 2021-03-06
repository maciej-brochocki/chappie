#!/usr/bin/env python
import sys
import cv2
from chappieEyes import Eyes
from chappieHead import Head
from chappieBrain import Brain


def print_help():
    print ""
    print "e - eyes postprocessing"
    print "h - head moves on/off"
    print "arrows - move head"
    print "b - brain mode"
    print "p - performance measurement"
    print "? - help"
    print "q - quit"


def chappie():
    # initialize
    performance = 0
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
        elif k == 84:
            head.move_up()
            head.update_position()
        elif k == 82:
            head.move_down()
            head.update_position()
        elif k == 83:
            head.move_left()
            head.update_position()
        elif k == 81:
            head.move_right()
            head.update_position()

    # clean up
    eyes.close()


if __name__ == '__main__':
    chappie()
    cv2.destroyAllWindows()
