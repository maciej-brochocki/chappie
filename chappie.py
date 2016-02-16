#!/usr/bin/env python
import sys
import cv2
import serial

# Screen Size Parameters
width = 320
height = 240
# Variables for keeping track of the current servo positions.
servoTiltPosition = 90
servoPanPosition = 90
# The pan/tilt servo ids for the Arduino serial command interface.
tiltChannel = 0
panChannel = 1
# These variables hold the x and y location for the middle of the detected face.
midFaceY = 0
midFaceX = 0
# The variables correspond to the middle of the screen, and will be compared to the midFace values
midScreenY = (height/2)
midScreenX = (width/2)
midScreenWindow = 10  # This is the acceptable 'error' for the center of the screen. 
# The degree of change that will be applied to the servo each time we update the position.
stepSize = 1

cameraDev = sys.argv[1]
video_capture = cv2.VideoCapture(cameraDev, width, height) # open video stream
cascadePath = sys.argv[2]
faceCascade = cv2.CascadeClassifier(cascadePath) # load detection description, here-> front face detection : "haarcascade_frontalface_alt.xml"
serialDev = sys.argv[3]
port = serial.Serial(serialDev, 57600) # Baud rate is set to 57600 to match the Arduino baud rate.
# Send the initial pan/tilt angles to the Arduino to set the device up to look straight forward.
port.write(tiltChannel)        # Send the Tilt Servo ID
port.write(servoTiltPosition)  # Send the Tilt Position (currently 90 degrees)
port.write(panChannel)         # Send the Pan Servo ID
port.write(servoPanPosition)   # Send the Pan Position (currently 90 degrees)

while True:
    # grab a new frame
    ret, frame = video_capture.read()
    # and convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    # proceed detection
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=2,
        minSize=(40, 40),
        flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING
    )
    # draw face area(s)
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # display the image
    cv2.imshow('Chappie', gray)
	
    # Find out if any faces were detected.
    if (len(faces) > 0)
        # If a face was found, find the midpoint of the first face in the frame.
        # NOTE: The .x and .y of the face rectangle corresponds to the upper left corner of the rectangle,
        #       so we manipulate these values to find the midpoint of the rectangle.
        midFaceY = faces[0].y + (faces[0].h/2)
        midFaceX = faces[0].x + (faces[0].w/2)
        # Find out if the Y component of the face is below the middle of the screen.
        if (midFaceY < (midScreenY - midScreenWindow))
            if (servoTiltPosition >= 5)
                servoTiltPosition -= stepSize # If it is below the middle of the screen, update the tilt position variable to lower the tilt servo.
        # Find out if the Y component of the face is above the middle of the screen.
        elif (midFaceY > (midScreenY + midScreenWindow))
            if (servoTiltPosition <= 175)
    		    servoTiltPosition += stepSize # Update the tilt position variable to raise the tilt servo.
        # Find out if the X component of the face is to the left of the middle of the screen.
        if (midFaceX < (midScreenX - midScreenWindow))
            if(servoPanPosition >= 5)
                servoPanPosition -= stepSize # Update the pan position variable to move the servo to the left.
        # Find out if the X component of the face is to the right of the middle of the screen.
        elif (midFaceX > (midScreenX + midScreenWindow))
            if(servoPanPosition <= 175)
                servoPanPosition += stepSize # Update the pan position variable to move the servo to the right.
        # Update the servo positions by sending the serial command to the Arduino.
        port.write(tiltChannel)        # Send the Tilt Servo ID
        port.write(servoTiltPosition)  # Send the Tilt Position (currently 90 degrees)
        port.write(panChannel)         # Send the Pan Servo ID
        port.write(servoPanPosition)   # Send the Pan Position (currently 90 degrees)
        time.sleep(0.001)
	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
