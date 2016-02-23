import cv2

class Eyes(object):
    # Screen Size Parameters
    width = 320
    height = 240
    # Camera device
    video_Capture = None
    # Preprocessing mode
    mode = 1

    def __init__(self, cameraDev):
        self.video_capture = cv2.VideoCapture(cameraDev) # open video stream
        self.video_capture.set(3, self.width)
        self.video_capture.set(4, self.height)
        return

    def look(self):
        # grab a new frame
        ret, frame = self.video_capture.read()
        # and convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.mode == 2:
            gray = cv2.equalizeHist(gray)
        elif self.mode == 3:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)
        return gray

    def close(self):
        # When everything is done, release the capture
        self.video_capture.release()
        return

    def setCfg(self, mode):
        self.mode = mode
        return

