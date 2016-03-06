import cv2
from subprocess import call

class Eyes(object):
    # Screen Size Parameters
    width = 320
    height = 240
    # Camera device
    video_Capture = None
    # Preprocessing mode
    mode = 0 # 0 - none, 1 - equalize hist, 2 - clahe

    def __init__(self, cameraDev):
        call("uvcdynctrl" + " -v -d video1 --set='Focus, Auto' 0", shell=True)
        call("uvcdynctrl" + " -v -d video1 --set='White Balance Temperature, Auto' 0", shell=True)
        call("uvcdynctrl" + " -v -d video1 --set='Exposure, Auto' 0", shell=True)
        self.video_capture = cv2.VideoCapture(cameraDev) # open video stream
        self.video_capture.set(3, self.width)
        self.video_capture.set(4, self.height)
        return

    def look(self):
        # grab a new frame
        ret, frame = self.video_capture.read()
        # and convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.mode == 1:
            gray = cv2.equalizeHist(gray)
        elif self.mode == 2:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)
        return gray

    def close(self):
        # When everything is done, release the capture
        self.video_capture.release()
        return

    def setCfg(self):
        self.mode = (self.mode + 1) % 3
        return

