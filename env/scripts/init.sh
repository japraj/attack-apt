#!/bin/bash
# This script should be run once every time the VM is started. It may be a good idea to set a cron job that does it for you

# Enable 1920x1080 resolution in VM
cvt 1920 1080 60
# If you get an error with xrandr, replace all the arguments that come after the --newmode flag with the output of the cvt command above
xrandr --newmode "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
xrandr --addmode Virtual1 "1920x1080_60.00"
xrandr --output Virtual1 --mode 1920x1080_60.00

# Start the Docker Daemon
sudo dockerd
