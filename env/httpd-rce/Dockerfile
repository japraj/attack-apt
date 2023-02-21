FROM httpd:2.4.49
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
RUN touch /usr/local/bin/vuln
RUN chmod 0777 /usr/local/bin/vuln
RUN apt-get update && apt-get install -y sudo
COPY sudoers /etc/sudoers
