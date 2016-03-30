import serial
import threading


class HeadThread(threading.Thread):
    port = None
    ctrl_frame = None

    def __init__(self, port, ctrl_frame):
        self.port = port
        self.ctrl_frame = ctrl_frame
        super(HeadThread, self).__init__()
        return

    def run(self):
        self.port.write(self.ctrl_frame)
        return


class Head(object):
    # Variables for keeping track of the current servo positions.
    servoTiltPosition = 60  # CHG: original 90, hw not straight!
    servoPanPosition = 90
    # The pan/tilt servo ids for the Arduino serial command interface.
    tiltChannel = 0
    panChannel = 1
    # The degree of change that will be applied to the servo each time we update the position.
    stepSize = 2
    # Serial device
    serialDev = ""
    port = None
    # Whether use Arduino
    enabled = 0
    thread = None

    def __init__(self, serial_dev, enabled=0):
        self.enabled = enabled
        self.serialDev = serial_dev
        if self.enabled > 0:
            self.port = serial.Serial(self.serialDev, 57600)  # Baud rate set to to match the Arduino baud rate.
        # Send the initial pan/tilt angles to the Arduino to set the device up to look straight forward.
        self.update_position()
        return

    def move_up(self):
        if self.enabled == 0:
            return 0
        if self.servoTiltPosition <= 175:
            self.servoTiltPosition += self.stepSize  # Update the tilt position variable to raise the tilt servo.
            return 1
        return 0

    def move_down(self):
        if self.enabled == 0:
            return 0
        if self.servoTiltPosition >= 5:
            self.servoTiltPosition -= self.stepSize  # Update the tilt position variable to lower the tilt servo.
            return 1
        return 0

    def move_left(self):
        if self.enabled == 0:
            return 0
        if self.servoPanPosition <= 175:  # CHG: hw reversed!
            self.servoPanPosition += self.stepSize  # Update the pan position variable to move the servo to the left.
            return 1
        return 0

    def move_right(self):
        if self.enabled == 0:
            return 0
        if self.servoPanPosition >= 5:  # CHG: hw reversed!
            self.servoPanPosition -= self.stepSize  # Update the pan position variable to move the servo to the right.
            return 1
        return 0

    def update_position(self):
        # Update the servo positions by sending the serial command to the Arduino.
        ctrl_frame = bytearray(4)
        ctrl_frame[0] = self.tiltChannel        # Send the Tilt Servo ID
        ctrl_frame[1] = self.servoTiltPosition  # Send the Tilt Position
        ctrl_frame[2] = self.panChannel         # Send the Pan Servo ID
        ctrl_frame[3] = self.servoPanPosition   # Send the Pan Position
        if self.enabled > 0:
            if self.thread is not None:
                self.thread.join()
            self.thread = HeadThread(self.port, ctrl_frame)
            self.thread.start()
        return

    def set_cfg(self):
        self.enabled = 1 - self.enabled
        print "head moves: ", self.enabled
        if self.enabled > 0:
            if self.port is None:
                self.port = serial.Serial(self.serialDev, 57600)  # Baud rate set to match the Arduino baud rate.
            self.servoTiltPosition = 60  # CHG: original 90, hw not straight!
            self.servoPanPosition = 90
            self.update_position()
        return
