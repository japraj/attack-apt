# Instructions, scripts, and binaries for setting up the artificial environment in which my APT runs

Directories:

- chained: Scripts that prepare the environment and chain the CVEs
- container-escape: Docker container escape exploit (CVE-2019-5736)
- httpd-rce: Remote Code Execution vuln in Apache httpd (CVE-2021-41773)
  Note: the container-escape/ and httpd-rce/ directories are stand-alone PoCs while chained/ combines them

Set up VM and install packages (one-time setup):

1. Install Debian 9 ISO https://www.debian.org/releases/stretch/debian-installer/
2. Create a VM with this ISO
3. Add yourself to sudo if necessary (test with `sudo echo "Hello"`) by following this link: https://unix.stackexchange.com/questions/179954/username-is-not-in-the-sudoers-file-this-incident-will-be-reported and then restarting the VM
4. `sudo apt-get install -y git` then `git clone` this repository
5. Download and install docker 18.09.1 static binary https://docs.docker.com/engine/install/binaries/ (the downloaded archive will contain runc version 1.0-rc6 too)
6. Make a copy of the runc binary named `runc-copy` in `~`
7. `apt-get install -y curl gcc`; we use `curl` for reproducing the httpd-rce exploit and `gcc` to compile the exploit binary in the container escape exploit
8. Run `sudo init.sh` every single time you start the VM - it modifies screen dimensions (1080x1920px) and starts the Docker daemon; note that you will need to run `chmod +x` on all scripts and executables
9. Build Python 3.10.6 (long operation):
   `cd ~` then `sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev` and then
   `wget https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tgz && tar -xvzf Python-3.10.6.tgz && cd Python-3.10.6 && ./configure --enable-optimizations --enable-shared --with-ensurepip=install && make -j8 && sudo make altinstall`, then finally add `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/Python-3.10.6/` to the bottom of `~/.bashrc`
10. `sudo docker image build -t httpd-rce $PATH` - note that you must modify `$PATH` to point to where-ever the `/httpd-rce` directory of the cloned repo is (e.g. `./attack-apt/env/httpd-rce/`)

Reproducing container escape:

1. `cd container-escape` and `sudo start_container.sh`, this will give you a terminal inside a docker container
2. Inside the terminal, run `exploit` (the binary will be copied by start_container.sh)
3. In another terminal, run `sudo docker exec pwnme bash` and you will get the output `No help topic for /usr/bin/bash` which indicates that the container escape was successful
4. You can verify this worked by checking that `ls /tmp` contains `escaped_container` and `less /usr/bin/runc` shows the contents of a script file near the top (followed by the original runc binary contents)

Reproducing httpd rce:

1. `docker run --name httpd-rce --rm -dit -p 3000:80 httpd-rce`
2. `sudo rce.sh`

Reproducing chained exploits (httpd RCE followed by container escape):

1. `start_httpd_container.sh`
2. In one terminal: `install_backdoor.sh`
3. In another terminal (after the `install_backdoor` script has had some time to run; if it gives you a terminal, just `exit` and run again): `sudo docker exec pwnme bash`
4. You can verify this worked by checking that `ls /tmp` contains `escaped_container`

Resources:

- https://ancat.github.io/exploitation/2019/02/16/cve-2019-5736.html
- https://github.com/ancat/scripts/blob/master/misc/runc-cve-2019-5736.c
- https://www.picussecurity.com/resource/blog/simulate-apache-cve-2021-41773-exploits-vulnerability
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41773
- https://attackerkb.com/topics/1RltOPCYqE/cve-2021-41773/rapid7-analysis?referrer=blog
- https://github.com/BlueTeamSteve/CVE-2021-41773
