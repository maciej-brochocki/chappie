import serial

class Head(object):
    # Variables for keeping track of the current servo positions.
    servoTiltPosition = 60 #CHG: original 90, hw not straight!
    servoPanPosition = 90
    # The pan/tilt servo ids for the Arduino serial command interface.
    tiltChannel = 0
    panChannel = 1
    # The degree of change that will be applied to the servo each time we update the position.
    stepSize = 1
    # Serial device
    serialDev = ""
    port = None
    # Whether use arduino
    enabled = 0

    def __init__(self, serialDev, enabled=0):
        self.enabled = enabled
        self.serialDev = serialDev
        if self.enabled > 0:
            self.port = serial.Serial(self.serialDev, 57600) # Baud rate is set to 57600 to match the Arduino baud rate.
        # Send the initial pan/tilt angles to the Arduino to set the device up to look straight forward.
        self.updatePosition()
        return

    def moveUp(self):
        if self.enabled == 0:
            return 0
        if self.servoTiltPosition <= 175:
            self.servoTiltPosition += self.stepSize # Update the tilt position variable to raise the tilt servo.
            return 1
        return 0

    def moveDown(self):
        if self.enabled == 0:
            return 0
        if self.servoTiltPosition >= 5:
            self.servoTiltPosition -= self.stepSize # Update the tilt position variable to lower the tilt servo.
            return 1
        return 0

    def moveLeft(self):
        if self.enabled == 0:
            return 0
        if self.servoPanPosition <= 175: #CHG: hw reversed!
            self.servoPanPosition += self.stepSize # Update the pan position variable to move the servo to the left.
            return 1
        return 0

    def moveRight(self):
        if self.enabled == 0:
            return 0
        if self.servoPanPosition >= 5: #CHG: hw reversed!
            self.servoPanPosition -= self.stepSize # Update the pan position variable to move the servo to the right.
            return 1
        return 0

    def updatePosition(self):
        # Update the servo positions by sending the serial command to the Arduino.
        ctrlFrame = bytearray(4)
        ctrlFrame[0] = self.tiltChannel        # Send the Tilt Servo ID
        ctrlFrame[1] = self.servoTiltPosition  # Send the Tilt Position
        ctrlFrame[2] = self.panChannel         # Send the Pan Servo ID
        ctrlFrame[3] = self.servoPanPosition   # Send the Pan Position
        if self.enabled > 0:
            self.port.write(ctrlFrame)
        return

    def setCfg(self):
        self.enabled = 1 - self.enabled
        if self.enabled > 0:
            if self.port == None:
                self.port = serial.Serial(self.serialDev, 57600) # Baud rate is set to 57600 to match the Arduino baud rate.
            self.servoTiltPosition = 60 #CHG: original 90, hw not straight!
            self.servoPanPosition = 90
            self.updatePosition()
        return
