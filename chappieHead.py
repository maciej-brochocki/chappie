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
    port = None
    # Don't use arduino
    dummy = 0
    serialDev = ""

    def __init__(self, serialDev, dummy=0):
        self.dummy = dummy
        self.serialDev = serialDev
        if self.dummy == 0:
            self.port = serial.Serial(self.serialDev, 57600) # Baud rate is set to 57600 to match the Arduino baud rate.
        # Send the initial pan/tilt angles to the Arduino to set the device up to look straight forward.
        self.updatePosition()
        return

    def moveUp(self):
        if self.servoTiltPosition <= 175:
            self.servoTiltPosition += self.stepSize # Update the tilt position variable to raise the tilt servo.
            self.updatePosition()
        return

    def moveDown(self):
        if self.servoTiltPosition >= 5:
            self.servoTiltPosition -= self.stepSize # Update the tilt position variable to lower the tilt servo.
            self.updatePosition()
        return

    def moveLeft(self):
        if self.servoPanPosition <= 175: #CHG: hw reversed!
            self.servoPanPosition += self.stepSize # Update the pan position variable to move the servo to the left.
            self.updatePosition()
        return

    def moveRight(self):
        if self.servoPanPosition >= 5: #CHG: hw reversed!
            self.servoPanPosition -= self.stepSize # Update the pan position variable to move the servo to the right.
            self.updatePosition()
        return

    def updatePosition(self):
        # Update the servo positions by sending the serial command to the Arduino.
        ctrlFrame = bytearray(4)
        ctrlFrame[0] = self.tiltChannel        # Send the Tilt Servo ID
        ctrlFrame[1] = self.servoTiltPosition  # Send the Tilt Position
        ctrlFrame[2] = self.panChannel         # Send the Pan Servo ID
        ctrlFrame[3] = self.servoPanPosition   # Send the Pan Position
        if self.dummy == 0:
            self.port.write(ctrlFrame)
        return

    def setCfg(self):
        self.dummy = 1 - self.dummy
        if self.dummy == 0 and self.port == None:
            self.port = serial.Serial(self.serialDev, 57600) # Baud rate is set to 57600 to match the Arduino baud rate.
        return

