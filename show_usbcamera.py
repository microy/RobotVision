#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Show the images from a USB camera
#

# External dependencies
import time
import cv2

# Enable video writing in to a file
videowriter_enabled = False
# Create a video writer object
videowriter = cv2.VideoWriter()
# Get the camera
camera = cv2.VideoCapture( 0 )
# Acquisition loop
while( True ) :
    # Capture image-by-image
    _, image = camera.read()
    # Write the image in the video file
    if videowriter_enabled : videowriter.write( image )
    # Display the resulting image
    cv2.imshow( 'USB Camera', image )
    # Keyboard interruption
    key = cv2.waitKey( 1 ) & 0xFF
    # Escape : quit the application
    if key == 27 : break
    # Space : save the image
    elif key == 32 :
        current_time = time.strftime( '%Y%m%d_%H%M%S' )
        print( 'Saving image {} to disk...'.format( current_time ) )
        cv2.imwrite( 'image-{}.png'.format( current_time ), image )
    # Enter : enable / disable video writing
    elif key == 10 :
        videowriter_enabled = not videowriter_enabled
        # Define the codec and the video parameters
        if videowriter_enabled :
            current_time = time.strftime( '%Y%m%d_%H%M%S' )
            print( 'Writing video {} to disk...'.format( current_time ) )
            videowriter.open( 'video-{}.avi'.format( current_time ), cv2.cv.CV_FOURCC( *'XVID' ), 30, ( 640, 480 ) )
        # Release the video writer object
        else : videowriter.release()
# Release the camera
camera.release()
# Close OpenCV windows
cv2.destroyAllWindows()
