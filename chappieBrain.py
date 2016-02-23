import cv2

class Brain(object):
    # The variables correspond to the middle of the screen, and will be compared to the midFace values
    midScreenX = 0
    midScreenY = 0
    midScreenWindow = 20  #CHG: original 10 # This is the acceptable 'error' for the center of the screen. 
    faceCascade = None
    head = None
    mode = 1

    def __init__(self, eyes, head, cascadePath):
        self.head = head
        self.midScreenX = eyes.width/2
        self.midScreenY = eyes.height/2
        self.faceCascade = cv2.CascadeClassifier(cascadePath) # load detection description, here-> front face detection : "haarcascade_frontalface_alt.xml"
        return

    def attention(self, frame):
        if self.mode == 1:
            objects = self.detectFaces(frame)
        elif self.mode == 2:
            objects = self.detectObjects(frame)
        self.visualizeObjects(frame, objects)
        self.reaction(objects)
        return

    def detectFaces(self, frame):
        # proceed detection
        return self.faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.2,
            minNeighbors=2,
            minSize=(40, 40),
            flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING
        )

    def detectObjects(self, frame):
        return []

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
            # If a face was found, find the midpoint of the first face in the frame.
            # NOTE: The .x and .y of the face rectangle corresponds to the upper left corner of the rectangle,
            #       so we manipulate these values to find the midpoint of the rectangle.
            # These variables hold the x and y location for the middle of the detected face.
            midFaceY = y + (h/2)
            midFaceX = x + (w/2)
            # Find out if the Y component of the face is below the middle of the screen.
            if midFaceY < (self.midScreenY - self.midScreenWindow):
                self.head.moveDown()
            # Find out if the Y component of the face is above the middle of the screen.
            elif midFaceY > (self.midScreenY + self.midScreenWindow):
                self.head.moveUp()
            # Find out if the X component of the face is to the left of the middle of the screen.
            if midFaceX < (self.midScreenX - self.midScreenWindow):
                self.head.moveLeft()
            # Find out if the X component of the face is to the right of the middle of the screen.
            elif midFaceX > (self.midScreenX + self.midScreenWindow):
                self.head.moveRight()
            break
        return

    def sleep(self):
        cv2.destroyAllWindows()
        return

    def setCfg(self, mode):
        self.mode = mode
        return

