import cv2
from subprocess import call


class Eyes(object):
    # Screen Size Parameters
    width = 320
    height = 240
    fps = 30
    # Camera device
    video_Capture = None
    # Pre-processing mode
    mode = 0  # 0 - none, 1 - equalize hist, 2 - clahe

    def __init__(self, camera_dev):
        call("uvcdynctrl -v -d video%d --set='Focus, Auto' 0" % camera_dev, shell=True)
        call("uvcdynctrl -v -d video%d --set='White Balance Temperature, Auto' 0" % camera_dev, shell=True)
        call("uvcdynctrl -v -d video%d --set='Exposure, Auto' 0" % camera_dev, shell=True)
        self.video_capture = cv2.VideoCapture(camera_dev)  # open video stream
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.width)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.height)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FPS, self.fps)
        return

    def look(self):
        # grab a new frame
        ret, frame = self.video_capture.read()
        # and convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.mode == 1:
            gray = cv2.equalizeHist(gray)
        elif self.mode == 2:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)
        return gray

    def close(self):
        # When everything is done, release the capture
        self.video_capture.release()
        return

    def set_cfg(self):
        self.mode = (self.mode + 1) % 3
        print "eyes mode: ", self.mode
        return
