import cv2
import numpy as np
from helpers import *

class Brain(object):
    head = None # head object
    mode = 0 # 0 - face detection, 1 - optical flow, 2 - objects
    # Mode 0 state:
    # The variables correspond to the middle of the screen, and will be compared to the midFace values
    midScreenX = 0
    midScreenY = 0
    midScreenWindow = 20  #CHG: original 10 # This is the acceptable 'error' for the center of the screen. 
    faceCascade = None
    # Mode 1 & 2 state:
    prvsFrame = None # store previous frame
    prvsObjects = [] # store previous objects

    def __init__(self, eyes, head, cascadePath):
        self.head = head
        self.midScreenX = eyes.width/2
        self.midScreenY = eyes.height/2
        self.faceCascade = cv2.CascadeClassifier(cascadePath) # load detection description, here-> front face detection : "haarcascade_frontalface_alt.xml"
        return

    def attention(self, frame):
        if self.mode == 0:
            frame, objects = self.detectFaces(frame)
        else:
            frame, objects = self.detectObjects(frame)
        self.visualizeObjects(frame, objects)
        self.reaction(objects)
        return

    def detectFaces(self, frame):
        # proceed detection
        return frame, self.faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.2,
            minNeighbors=2,
            minSize=(40, 40),
            flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING
        )

    def detectObjects(self, frame):
        newFrame = frame
        objects = []
        if self.prvsFrame != None:
            flow = cv2.calcOpticalFlowFarneback(self.prvsFrame, frame, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            mag = np.uint8(mag)
            if self.mode == 1:
                # fancy colours
                hsv = np.zeros(frame.shape + (3,), dtype=np.uint8)
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,1] = 255
                #hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                hsv[...,2] = np.minimum(mag*4, 255)
                newFrame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            elif self.mode == 2:
                # binary
                ret, newFrame = cv2.threshold(mag,2,255,cv2.THRESH_BINARY)
                kernel = np.ones((5,5),np.uint8)
                newFrame = cv2.dilate(newFrame,kernel,iterations = 10)
                contours,hierarchy = cv2.findContours(newFrame, 1, 2)
                for cnt in contours:
                    objects.append(cv2.boundingRect(cnt))
                objects = mergeAreas([], objects)
                if len(objects):
                    self.prvsObjects = objects
                else:
                    objects = self.prvsObjects
                newFrame = frame.copy()
        self.prvsFrame = frame
        return newFrame, objects

    def visualizeObjects(self, frame, objects):
        # draw face area(s)
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # display the image
        cv2.imshow('Chappie', frame)
        return

    def reaction(self, objects):
        # Find out if any faces were detected.
        for (x, y, w, h) in objects:
            change = 0
            # If a face was found, find the midpoint of the first face in the frame.
            # NOTE: The .x and .y of the face rectangle corresponds to the upper left corner of the rectangle,
            #       so we manipulate these values to find the midpoint of the rectangle.
            # These variables hold the x and y location for the middle of the detected face.
            midFaceY = y + (h/2)
            midFaceX = x + (w/2)
            # Find out if the Y component of the face is below the middle of the screen.
            if midFaceY < (self.midScreenY - self.midScreenWindow):
                change += self.head.moveDown()
            # Find out if the Y component of the face is above the middle of the screen.
            elif midFaceY > (self.midScreenY + self.midScreenWindow):
                change += self.head.moveUp()
            # Find out if the X component of the face is to the left of the middle of the screen.
            if midFaceX < (self.midScreenX - self.midScreenWindow):
                change += self.head.moveLeft()
            # Find out if the X component of the face is to the right of the middle of the screen.
            elif midFaceX > (self.midScreenX + self.midScreenWindow):
                change += self.head.moveRight()
            if change > 0:
                self.head.updatePosition()
                self.resetDetector()
            break
        return

    def sleep(self):
        cv2.destroyAllWindows()
        return

    def setCfg(self):
        self.mode = (self.mode + 1) % 3
        return

    def resetDetector(self):
        self.prvsFrame = None
        self.prvsObjects = []

