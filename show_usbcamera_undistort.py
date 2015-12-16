#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Show the images from a USB camera
#

# External dependencies
import pickle
import cv2

# Load calibration file
with open( 'calibration.pkl', 'rb' ) as calibration_file :
    calibration = pickle.load( calibration_file )
# Get the camera
camera = cv2.VideoCapture( 0 )
# Acquisition loop
while( True ) :
    # Capture image-by-image
    _, image = camera.read()
    # Undistort the image
    image = cv2.remap( image, calibration['undistort_map'][0], calibration['undistort_map'][1], cv2.INTER_LINEAR )
    # Print ROI
    cv2.rectangle( image, calibration['roi'][:2], calibration['roi'][2:], (0,0,255), 2 )
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
