# Instructions, scripts, and binaries for setting up the artificial environment in which my APT runs
Directories:
- scripts: Scripts that prepare the environment
- container-escape: Docker container escape exploit (CVE-2019-5736)
- httpd-rce: Remote Code Execution vuln in Apache httpd (CVE-2021-41773)

Set up VM and install packages (one-time setup):
1) Install Debian 9 ISO
2) Download correct versions of docker and runc
3) Make a copy of the runc binary named `runc-copy` in `~`
4) Install `gcc`

Set up environment for being attacked:
1) Run `init.sh` when you first start the VM
2) Run `start_container.sh`, this will give you a terminal
3) Inside the terminal, run `./exploit` (the binary will be copied by start_container.sh)
4) In another terminal, run `sudo docker exec pwnme bash`