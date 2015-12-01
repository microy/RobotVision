#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Application to calibrate a camera
#

# External dependencies
import glob
import Calibration

# Calibration pattern size
pattern_size = ( 9, 6 )
# Calibrate the camera
calibration = Calibration.CalibrateCamera( glob.glob( 'image-*.png' ), pattern_size )
# Write the calibration
Calibration.SaveCalibration( calibration, 'calibration.pkl' )
Calibration.SaveCalibrationLog( calibration, 'calibration.log' )
print( 'Calibration error : {}'.format( calibration['calib_error'] ) )
print( 'Reprojection error : {}'.format( calibration['reproject_error'] ) )
print( 'Camera matrix :\n{}'.format( calibration['camera_matrix'] ) )
print( 'Distortion coefficients :\n{}'.format( calibration['dist_coefs'].ravel() ) )
