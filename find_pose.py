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
# Chessboard pattern
pattern_points = np.zeros( ( np.prod( pattern_size ), 3 ), np.float32 )
pattern_points[ :, :2 ] = np.indices( pattern_size ).T.reshape( -1, 2 )
# Chessboard square size
pattern_points *= 34.15
# 3D points
object_points = []
# 2D points
image_points = []
# Load calibration file
with open( 'calibration.pkl', 'rb' ) as calibration_file :
    calibration = pickle.load( calibration_file )
# Read the image
image = cv2.imread( 'pose-estimation.png' )
# Get image size
image_size = image.shape[ :2 ][ ::-1 ]
# Compute new optimal camera matrix
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix( calibration['camera_matrix'], calibration['dist_coefs'], image_size, 1, image_size )
# Remove lens distortion
rectified_image = cv2.undistort( image, calibration['camera_matrix'], calibration['dist_coefs'], None, new_camera_matrix )
print calibration['camera_matrix']
print new_camera_matrix
print roi
# Print ROI
#cv2.rectangle( rectified_image, roi[:2], roi[2:], (0,0,255), 2 )
#cv2.imshow( 'rectified', rectified_image )
#cv2.waitKey()
# Convert the image in grayscale
rectified_image = cv2.cvtColor( rectified_image, cv2.COLOR_BGR2GRAY )
# Chessboard detection flags
flags  = 0
flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
flags |= cv2.CALIB_CB_NORMALIZE_IMAGE
# Find the chessboard corners on the image
found, corners = cv2.findChessboardCorners( rectified_image, pattern_size, flags = flags )
# Pattern not found
if not found : print( 'Chessboard not found...' )
# Termination criteria for the corner detection
criteria = ( cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 1e-5 )
# Refine the corner positions
cv2.cornerSubPix( rectified_image, corners, ( 11, 11 ), ( -1, -1 ), criteria )
# Pose estimation flags
flags = 0
#flags = CV_ITERATIVE
#flags = CV_P3P
#flags = CV_EPNP
# Solve the pose
_, rotation_vector, translation_vector = cv2.solvePnP( pattern_points, corners.reshape( -1, 2 ), calibration['camera_matrix'], calibration['dist_coefs'] )
print rotation_vector
print translation_vector
rotation_matrix, _ = cv2.Rodrigues( rotation_vector )
print rotation_matrix
