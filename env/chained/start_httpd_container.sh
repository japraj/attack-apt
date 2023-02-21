#!/bin/bash
# Similar to container-escape/start_container.sh but the container does not
# have a copy of the exploit, it is just vulnerable to the httpd RCE vuln. 
# Assumes an unmodified copy of the runc binary exists at ~/runc-copy

# Copy the "good" runc binary
sudo cp ~/runc-copy /usr/bin/runc

# Stop any running container with the same name
sudo docker stop pwnme

# Start the pwnme container
sudo docker run --name pwnme --rm -p 3000:80 -dit httpd-rce
