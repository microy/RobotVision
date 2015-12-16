#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Application to calibrate a camera
#

# External dependencies
import glob
import pickle
import numpy as np
import cv2

# Chessboard pattern size
pattern_size = ( 9, 6 )
# Chessboard pattern points
pattern_points = np.zeros( ( np.prod( pattern_size ), 3 ), np.float32 )
pattern_points[ :, :2 ] = np.indices( pattern_size ).T.reshape( -1, 2 )
# Chessboard square size (in mm)
pattern_points *= 34.15
# 3D points
object_points = []
# 2D points
image_points = []
# Get the chessboard image files
image_files = glob.glob( 'calibration-*.png' )
# Chessboard detection flags
flags  = 0
flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
flags |= cv2.CALIB_CB_NORMALIZE_IMAGE
# Termination criteria for the corner detection
criteria = ( cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 1e-5 )
# Find the chessboard on each image
for filename in image_files :
	# Load the image
	image = cv2.imread( filename )
	# Convert the image in grayscale
	image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
	# Find the chessboard corners on the image
	found, corners = cv2.findChessboardCorners( image, pattern_size, flags = flags )
	# Pattern not found
	if not found :
		print( 'Chessboard not found on image {}...'.format( filename ) )
		continue
	# Refine the corner positions
	cv2.cornerSubPix( image, corners, ( 11, 11 ), ( -1, -1 ), criteria )
	# Store image and corner informations
	image_points.append( corners.reshape( -1, 2 ) )
	object_points.append( pattern_points )
# Get image size
image_size = cv2.imread( image_files[ 0 ] ).shape[ :2 ][ ::-1 ]
# Camera calibration flags
flags  = 0
#flags |= cv2.CALIB_USE_INTRINSIC_GUESS
#flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
#flags |= cv2.CALIB_FIX_ASPECT_RATIO
#flags |= cv2.CALIB_ZERO_TANGENT_DIST
flags |= cv2.CALIB_RATIONAL_MODEL
#flags |= cv2.CALIB_FIX_K1
#flags |= cv2.CALIB_FIX_K2
#flags |= cv2.CALIB_FIX_K3
#flags |= cv2.CALIB_FIX_K4
#flags |= cv2.CALIB_FIX_K5
# Camera calibration
calibration = cv2.calibrateCamera( object_points, image_points, image_size, flags = flags )
# Store the calibration results in a dictionary
parameter_names = ( 'calib_error', 'camera_matrix', 'dist_coefs', 'rvecs', 'tvecs' )
calibration = dict( zip( parameter_names, calibration ) )
# Compute optimal camera matrix
calibration['new_camera_matrix'], calibration['roi'] = cv2.getOptimalNewCameraMatrix( calibration['camera_matrix'], calibration['dist_coefs'],
    image_size, 1, image_size )
# Compute undistortion maps
calibration['undistort_map'] = cv2.initUndistortRectifyMap( calibration['camera_matrix'], calibration['dist_coefs'],
    None, calibration['new_camera_matrix'], image_size, cv2.CV_32FC1 )
# Write the calibration object with all the parameters
with open( 'calibration.pkl', 'wb' ) as calibration_file :
	pickle.dump( calibration, calibration_file, pickle.HIGHEST_PROTOCOL )
# Print the result
print( 'Calibration error : {}'.format( calibration['calib_error'] ) )
print( 'Camera matrix :\n{}'.format( calibration['camera_matrix'] ) )
print( 'Distortion coefficients :\n{}'.format( calibration['dist_coefs'].ravel() ) )
print( 'New camera matrix :\n{}'.format( calibration['new_camera_matrix'] ) )
print( 'ROI :\n{}'.format( calibration['roi'] ) )
