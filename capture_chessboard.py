#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Capture calibration chessboard
#

# External dependencies
import time
import cv2
import Calibration

# Calibration pattern size
pattern_size = ( 9, 6 )
# Get the camera
camera = cv2.VideoCapture( 1 )
# Acquisition loop
while( True ) :
    # Capture image-by-image
    _, image = camera.read()
    # Display the chessboard on the image
    chessboard = Calibration.PreviewChessboard( image, pattern_size )
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
		cv2.imwrite( 'image-{}.png'.format( current_time ), image )
# Release the camera
camera.release()
# Close OpenCV windows
cv2.destroyAllWindows()
