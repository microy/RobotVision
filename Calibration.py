# -*- coding:utf-8 -*-

#
# Camera calibration module
#

# External dependencies
import math
import os
import pickle
import cv2
import numpy as np

# Create the calibration directory
def CreateCalibrationDirectory( folder ) :
	try : os.makedirs( folder )
	except OSError :
		if not os.path.isdir( folder ) : raise

# Load the calibration parameters from a file
def LoadCalibration( filename ) :
	calibration = None
	if os.path.isfile( filename ) :
		with open( filename, 'rb' ) as calibration_file :
			calibration = pickle.load( calibration_file )
	return calibration

# Save the calibration parameters to a file
def SaveCalibration( calibration, filename ) :
	# Write the calibration object with all the parameters
	with open( filename, 'wb' ) as calibration_file :
		pickle.dump( calibration, calibration_file, pickle.HIGHEST_PROTOCOL )

# Save the calibration parameters to a file
def SaveCalibrationLog( calibration, filename ) :
	# Write calibration results
	with open( filename, 'w' ) as output_file :
		output_file.write( '~~~ Camera calibration ~~~\n\n' )
		output_file.write( 'Calibration error : {}\n'.format( calibration['calib_error'] ) )
		output_file.write( 'Reprojection error : {}\n'.format( calibration['reproject_error'] ) )
		output_file.write( 'Camera matrix :\n{}\n'.format( calibration['camera_matrix'] ) )
		output_file.write( 'Distortion coefficients :\n{}'.format( calibration['dist_coefs'].ravel() ) )

# Find the chessboard quickly, and draw it
def PreviewChessboard( image, pattern_size ) :
	# Find the chessboard corners on the image
	found, corners = cv2.findChessboardCorners( image, pattern_size, flags = cv2.CALIB_CB_FAST_CHECK )
	# Draw the chessboard corners on the image
	if found : cv2.drawChessboardCorners( image, pattern_size, corners, found )

# Camera calibration
def CalibrateCamera( image_files, pattern_size ) :
	# Chessboard pattern
	pattern_points = np.zeros( ( np.prod( pattern_size ), 3 ), np.float32 )
	pattern_points[ :, :2 ] = np.indices( pattern_size ).T.reshape( -1, 2 )
	# Get image size
	height, width = cv2.imread( image_files[0] ).shape[:2]
	img_size = ( width, height )
	# 3D points
	obj_points = []
	# 2D points
	img_points = []
	# Images with chessboard found
	img_files = []
	# For each image
	for filename in image_files :
		# Load the image
		image = cv2.imread( filename )
		# Chessboard detection flags
		flags  = 0
		flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
		flags |= cv2.CALIB_CB_NORMALIZE_IMAGE
		# Find the chessboard corners on the image
		found, corners = cv2.findChessboardCorners( image, pattern_size, flags = flags )
		# Pattern not found
		if not found :
			print( 'Chessboard not found on image {}...'.format( filename ) )
			continue
		# Convert the image in grayscale
		image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
		# Termination criteria
		criteria = ( cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 1e-5 )
		# Refine the corner positions
		cv2.cornerSubPix( image, corners, (11, 11), (-1, -1), criteria )
		# Store image and corner informations
		img_points.append( corners.reshape(-1, 2) )
		obj_points.append( pattern_points )
		img_files.append( filename )
	# Camera calibration flags
	flags  = 0
#	flags |= cv2.CALIB_USE_INTRINSIC_GUESS
#	flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
#	flags |= cv2.CALIB_FIX_ASPECT_RATIO
#	flags |= cv2.CALIB_ZERO_TANGENT_DIST
	flags |= cv2.CALIB_RATIONAL_MODEL
#	flags |= cv2.CALIB_FIX_K3
	flags |= cv2.CALIB_FIX_K4
	flags |= cv2.CALIB_FIX_K5
	# Camera calibration
	calibration = cv2.calibrateCamera( obj_points, img_points, img_size, flags = flags )
	# Store the calibration results in a dictionary
	parameter_names = ( 'calib_error', 'camera_matrix', 'dist_coefs', 'rvecs', 'tvecs' )
	calibration = dict( zip( parameter_names, calibration ) )
	# Compute reprojection error
	calibration['reproject_error'] = 0
	for i, obj in enumerate( obj_points ) :
		# Reproject the object points using the camera parameters
		reprojected_img_points, _ = cv2.projectPoints( obj, calibration['rvecs'][i],
		      calibration['tvecs'][i], calibration['camera_matrix'], calibration['dist_coefs'] )
		# Compute the error with the original image points
		error = cv2.norm( img_points[i], reprojected_img_points.reshape(-1, 2), cv2.NORM_L2 )
		# Add to the total error
		calibration['reproject_error'] += error ** 2
	calibration['reproject_error'] = math.sqrt( calibration['reproject_error'] / ( len( obj_points ) * np.prod( pattern_size ) ) )
	# Backup calibration parameters for future use
	calibration['img_points'] = img_points
	calibration['obj_points'] = obj_points
	calibration['img_size'] = img_size
	calibration['img_files'] = img_files
	calibration['pattern_size'] = pattern_size
	# Return the results of the calibration
	return calibration
