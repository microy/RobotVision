#! /bin/sh

#
# Configure the stereo USB cameras
#

# Camera device
CAMERA = video0

# Disable autofocus
uvcdynctrl -v -d $CAMERA --set='Focus, Auto' 0

# Fix the focus
uvcdynctrl -v -d $CAMERA --set='Focus (absolute)' 30
