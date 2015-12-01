#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Capture calibration circles
#

# External dependencies
import cv2
import numpy as np

# Get the camera
camera = cv2.VideoCapture( 0 )
# Acquisition loop
while( True ) :
    # Capture image-by-image
    _, image = camera.read()
    # Convert it to gray
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    # Smooth it, otherwise a lot of false circles may be detected
    gray = cv2.GaussianBlur( gray, ( 9, 9 ), 2, 2 )
    # Detect the circles
    circles = cv2.HoughCircles( gray, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 20 )
    # Display the circles if found
    if circles is not None :
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round( circles[ 0, : ] ).astype( int )
        for ( x, y, r ) in circles :
            cv2.circle( image, ( x, y ), 3, ( 0, 255, 0 ), -1, 8, 0 )
            cv2.circle( image, ( x, y ), r, ( 0, 0, 255 ), 3, 8, 0 )
    # Display the resulting image
    cv2.imshow( 'USB Camera', image )
    # Keyboard interruption
    key = cv2.waitKey( 1 ) & 0xFF
    # Escape : quit the application
    if key == 27 : break
# Release the camera
camera.release()
# Close OpenCV windows
cv2.destroyAllWindows()
