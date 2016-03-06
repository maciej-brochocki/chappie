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
    midScreenWindow = 20  # CHG: original 10 # This is the acceptable 'error' for the center of the screen.
    faceCascade = None
    smileCascade = None
    # Mode 1 & 2 state:
    prvsFrame = None # store previous frame
    prvsObjects = [] # store previous objects

    def __init__(self, eyes, head):
        self.head = head
        self.midScreenX = eyes.width/2
        self.midScreenY = eyes.height/2
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml") # load detection description
        self.smileCascade = cv2.CascadeClassifier("haarcascade_smile.xml") # load detection description
        return

    def attention(self, frame):
        if self.mode == 0:
            frame, objects = self.detectFaces(frame)
        elif self.mode == 1:
            frame, objects = self.detectFlow(frame)
        elif self.mode == 2:
            frame, objects = self.detectObjects(frame)
        self.visualizeObjects(frame, objects)
        self.reaction(objects)
        return

    def detectFaces(self, frame):
        # proceed detection
        smiles = [[]]
        faces = self.faceCascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(40, 40), flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING)
        # sort faces so we get the biggest first
        if len(faces)>0:
            faces = sortObjectsByIndex(faces, faces[:,2]*faces[:,3])
        for x1, y1, w1, h1 in faces:
            # look for smile inside face
            roi = frame[y1:(y1+h1), x1:(x1+w1)]
            result = self.smileCascade.detectMultiScale(roi, scaleFactor=1.3, minNeighbors=4, minSize=(15, 15), flags=cv2.CASCADE_SCALE_IMAGE)
            for x2, y2, w2, h2 in result:
                if len(smiles[0]) == 0:
                    smiles = [[x1+x2, y1+y2, w2, h2]]
                else:
                    smiles = np.vstack((smiles, [x1+x2, y1+y2, w2, h2]))
        # put smiles first, so we prefer happy people
        if len(smiles[0]) > 0:
            faces = np.vstack((smiles, faces))
        return frame, faces

    def computeOpticalFlow(self, frame):
        # get optical flow
        flow = cv2.calcOpticalFlowFarneback(self.prvsFrame, frame, 0.5, 3, 15, 3, 5, 1.2, 0)
        fx, fy = flow[:, :, 0], flow[:, :, 1]
        # become independent of camera moves
        fx -= np.median(fx)
        fy -= np.median(fy)
        # convert to polar as more useful
        mag, ang = cv2.cartToPolar(fx, fy)
        mag = np.uint8(mag)
        return fx, fy, ang, mag

    def detectFlow(self, frame):
        newFrame = frame
        objects = []
        if self.prvsFrame != None:
            fx, fy, ang, mag = self.computeOpticalFlow(frame)
            # fancy colours
            hsv = np.zeros(frame.shape + (3,), dtype=np.uint8)
            hsv[...,0] = ang*180/np.pi/2
            hsv[...,1] = 255
            hsv[...,2] = np.minimum(mag*4, 255) # cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            newFrame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            # dummy object for average flow
            objects = [(self.midScreenX + int(np.sum(fx)/1000), self.midScreenY + int(np.sum(fy)/1000), 2, 2)]
        self.prvsFrame = frame
        return newFrame, objects

    def detectObjects(self, frame):
        newFrame = frame
        objects = []
        if self.prvsFrame != None:
            fx, fy, ang, mag = self.computeOpticalFlow(frame)
            # convert to binary image
            ret, newFrame = cv2.threshold(mag,2,255,cv2.THRESH_BINARY)
            # join close objects
            kernel = np.ones((5,5),np.uint8)
            newFrame = cv2.dilate(newFrame,kernel,iterations = 10)
            # get objects
            contours,hierarchy = cv2.findContours(newFrame, 1, 2)
            # convert them to rectangles
            for cnt in contours:
                objects.append(cv2.boundingRect(cnt))
            # join rectangles if they overlap
            objects = mergeAreas([], objects)
            # return previous bigger rectangle if applicable
            objects = overlappingAreas(objects, self.prvsObjects)
            # sort objects so we get the biggest first
            #if len(objects)>0:
            #    objects = np.hstack((objects, np.reshape(objects[:,2]*objects[:,3],(-1,1))))
            #    objects.view('i32,i32,i32,i32,i32').sort(order=['f4'], axis=0)
            #    objects = objects[:,0:4]
            #    objects = objects[::-1]
            # return previous results if nothing detected
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
                self.resetDetectors()
            break
        return

    def sleep(self):
        cv2.destroyAllWindows()
        return

    def setCfg(self):
        self.mode = (self.mode + 1) % 3
        self.resetDetectors()
        return

    def resetDetectors(self):
        self.prvsFrame = None
        self.prvsObjects = []
