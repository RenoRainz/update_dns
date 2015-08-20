##############
# DNS Update #
##############

FROM centos:7

MAINTAINER RenoRainz

ENV DATA_DIR=/app  BIND_USER=bind 

# Software installation
RUN yum update -y && yum install -y bind python perl perl-Net-SSLeay openssl 
COPY ./source/rpms/webmin-1.760-1.noarch.rpm /tmp/
RUN rpm -ivh /tmp/webmin-1.760-1.noarch.rpm
RUN rm -rf /tmp/webmin-1.760-1.noarch.rpm

# Create directory and put config file
RUN mkdir -p /app/update_dns
COPY ./source/app/update_dns.py /app/update_dns.py
RUN chmod 755 /app/update_dns.py

COPY ./source/etc/init.d/entrypoint.sh /etc/init.d/entrypoint.sh
RUN chmod 755 /etc/init.d/entrypoint.sh

EXPOSE 53/udp 10000/tcp
#VOLUME ["${DATA_DIR}"]
ENTRYPOINT ["/etc/init.d/entrypoint.sh"]
#ENTRYPOINT ["/bin/bash"]