#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Pose estimation of the camera
#

# External dependencies
import pickle
import cv2
import numpy as np

# Calibration pattern size
pattern_size = ( 9, 6 )
# Load calibration file
with open( 'calibration.pkl', 'rb' ) as calibration_file :
    calibration = pickle.load( calibration_file )
# Get the camera
camera = cv2.VideoCapture( 0 )
# Change the camera resolution
#camera.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920 )
#camera.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1200 )
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
    # Space : save the image and quit
    elif key == 32 :
        cv2.imwrite( 'pose-estimation.png', image )
        break
# Release the camera
camera.release()
# Close OpenCV windows
cv2.destroyAllWindows()
# Chessboard pattern
pattern_points = np.zeros( ( np.prod( pattern_size ), 3 ), np.float32 )
pattern_points[ :, :2 ] = np.indices( pattern_size ).T.reshape( -1, 2 )
# 3D points
object_points = []
# 2D points
image_points = []
# Convert the image in grayscale
image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
# Chessboard detection flags
flags  = 0
flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
flags |= cv2.CALIB_CB_NORMALIZE_IMAGE
# Find the chessboard corners on the image
found, corners = cv2.findChessboardCorners( image, pattern_size, flags = flags )
# Pattern not found
if not found : print( 'Chessboard not found...' )
# Termination criteria for the corner detection
criteria = ( cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 1e-5 )
# Refine the corner positions
cv2.cornerSubPix( image, corners, ( 11, 11 ), ( -1, -1 ), criteria )
# Pose estimation flags
flags = 0
#flags = CV_ITERATIVE
#flags = CV_P3P
#flags = CV_EPNP
# Solve the pose
ret, rvec, tvec = cv2.solvePnP( pattern_points, corners.reshape( -1, 2 ), calibration['camera_matrix'], calibration['dist_coefs'] ) #,
#    calibration['rvecs'], calibration['tvecs'], True, flags )
print ret
print rvec
print tvec
