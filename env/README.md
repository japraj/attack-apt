# Instructions, scripts, and binaries for setting up the artificial environment in which my APT runs
Directories:
- chained: Scripts that prepare the environment and chain the CVEs
- container-escape: Docker container escape exploit (CVE-2019-5736)
- httpd-rce: Remote Code Execution vuln in Apache httpd (CVE-2021-41773)
Note: the container-escape/ and httpd-rce/ directories are stand-alone PoCs while chained/ combines them

Set up VM and install packages (one-time setup):
1) Install Debian 9 ISO
2) Download correct versions of docker and runc
3) Make a copy of the runc binary named `runc-copy` in `~`
4) Install `gcc` and `curl`
5) Clone this repo into the VM
6) Run `init.sh` every single time you start the VM - it modifies screen dimensions (1080x1920px) and starts the Docker daemon 
7) `docker image build -t httpd-rce $PATH` - note that you must modify `$PATH` to point to where-ever the `/httpd-rce` directory of the cloned repo is (e.g. `./attack-apt/env/httpd-rce/`)

Reproducing container escape:
1) `start_container.sh`, this will give you a terminal
2) Inside the terminal, run `exploit` (the binary will be copied by start_container.sh)
3) In another terminal, run `sudo docker exec pwnme bash`
4) You can verify this worked by checking that `ls /tmp` contains `escaped_container`

Reproducing httpd rce:
1) `docker run --name httpd-rce --rm -dit -p 3000:80 httpd-rce`
2) `rce.sh`

Reproducing chained exploits (httpd RCE followed by container escape):
1) `start_httpd_container.sh`
2) In one terminal: `install_backdoor.sh`
3) In another terminal (after the `install_backdoor` script has had some time to run; if it gives you a terminal, just `exit` and run again): `sudo docker exec pwnme bash`
4) You can verify this worked by checking that `ls /tmp` contains `escaped_container`

Resources:
- https://ancat.github.io/exploitation/2019/02/16/cve-2019-5736.html
- https://github.com/ancat/scripts/blob/master/misc/runc-cve-2019-5736.c
- https://www.picussecurity.com/resource/blog/simulate-apache-cve-2021-41773-exploits-vulnerability
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41773
- https://attackerkb.com/topics/1RltOPCYqE/cve-2021-41773/rapid7-analysis?referrer=blog
- https://github.com/BlueTeamSteve/CVE-2021-41773
