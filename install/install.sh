#!/bin/bash
# Install the script as WSGI app for Apache2
apt install libapache2-mod-wsgi-py3

mkdir /etc/pwnboard
cp topology.json /etc/pwnboard/
cp config.yml /etc/pwnboard/

logfile=`grep "logfile:" /etc/config.yml | awk '{print $2}'`

touch $logfile
chown www-data:www-data $logfile

cp ./install/pwnboard.wsgi ./
cp ./install/pwnboard.conf /etc/apache2/sites-available/

a2ensite pwnboard
service apache2 restart

