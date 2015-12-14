#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Capture calibration chessboard
#

# External dependencies
import time
import cv2
import numpy as np

# Calibration pattern size
pattern_size = ( 9, 6 )
# Get the camera
camera = cv2.VideoCapture( 0 )
# Acquisition loop
while( True ) :
    # Capture image-by-image
    _, image = camera.read()
    # Copy the image for display
    chessboard = np.copy( image )
    # Find the chessboard corners on the image
    found, corners = cv2.findChessboardCorners( chessboard, pattern_size, flags = cv2.CALIB_CB_FAST_CHECK )
    # Draw the chessboard corners on the image
    if found : cv2.drawChessboardCorners( chessboard, pattern_size, corners, found )
    # Display the resulting image
    cv2.imshow( 'USB Camera', chessboard )
    # Keyboard interruption
    key = cv2.waitKey( 1 ) & 0xFF
    # Escape : quit the application
    if key == 27 : break
    # Space : save the image
    elif key == 32 :
        current_time = time.strftime( '%Y%m%d_%H%M%S' )
        print( 'Save image {} to disk...'.format( current_time ) )
        cv2.imwrite( 'calibration-{}.png'.format( current_time ), image )
# Release the camera
camera.release()
# Close OpenCV windows
cv2.destroyAllWindows()
