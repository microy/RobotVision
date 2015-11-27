#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Show the images from a USB camera
#

# External dependencies
import cv2

# The camera
camera = cv2.VideoCapture( 1 )

# Acquisition loop
while( True ) :

    # Capture frame-by-frame
    _, image = camera.read()

    # Display the resulting frame
    cv2.imshow( 'USB Camera', image )
    if cv2.waitKey( 1 ) & 0xFF == 27 :
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
