#!/bin/bash
# Starts a pwnable container. Assumes an unmodified copy of the runc binary exists at ~/runc-copy

# Copy the "good" runc binary
sudo cp ~/runc-copy /usr/bin/runc

# Re-compile the exploit so we always use the latest version
gcc -o ~/exploit exploit.c

# Start the pwnme container and copy the exploit binary to it
sudo docker run --name pwnme --rm -dit ubuntu:22.04 bash
sudo docker cp ~/exploit pwnme:/exploit
sudo docker attach pwnme