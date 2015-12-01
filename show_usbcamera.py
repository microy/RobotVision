#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Show the images from a USB camera
#

# External dependencies
import cv2

# Get the camera
camera = cv2.VideoCapture( 0 )
# Acquisition loop
while( True ) :
    # Capture image-by-image
    _, image = camera.read()
    # Display the resulting image
    cv2.imshow( 'USB Camera', image )
    # Keyboard interruption with Escape
    if cv2.waitKey( 1 ) & 0xFF == 27 : break
# Release the camera
camera.release()
# Close OpenCV windows
cv2.destroyAllWindows()
