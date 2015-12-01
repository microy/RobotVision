#! /bin/sh

#
# Configure the USB camera
#

# Disable autofocus
uvcdynctrl -v -d video0 --set='Focus, Auto' 0

# Fix the focus
uvcdynctrl -v -d video0 --set='Focus (absolute)' 0

# Fix the power line frequency
uvcdynctrl -v -d video0 --set='Power Line Frequency' 1
