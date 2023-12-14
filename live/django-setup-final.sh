#!/bin/sh
APPFOLDERPATH=`pwd`
APPNAME=$1
DOMAINNAME=$2
pname=$3
if [ "$APPNAME" = "" ] || [ "$DOMAINNAME" = "" ] || [ "$pname" = "" ]; then
    echo "Usage:"
    echo "  $ set_up.sh <project> <domain> <pname>"
    exit 1
fi
apt-update
apt-get -y install python3-dev python3-pip nginx
pip3 install --upgrade pip
pip3 install virtualenv
virtualenv myprojectenv
. ./myprojectenv/bin/activate
pip install django gunicorn 
REQ=`find . -type f -name requirement*.txt`
pip install -r $REQ 

deactivate


cat > /etc/systemd/system/${APPNAME}.socket << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/${APPNAME}.sock

[Install]
WantedBy=sockets.target
EOF

cat > /etc/systemd/system/${APPNAME}.service << EOF
[Unit]
Description=gunicorn daemon
Requires=${APPNAME}.socket
After=network.target

[Service]           
User=root
Group=root
WorkingDirectory=${APPFOLDERPATH}
ExecStart=${APPFOLDERPATH}/myprojectenv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/${APPNAME}.sock \\
          ${pname}.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/nginx/sites-available/${APPNAME} << EOF

server {
    listen 80;
    server_name ${DOMAINNAME};

location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root ${APPFOLDERPATH};
    }

location / {
        include proxy_params;
        proxy_pass http://unix:/run/${APPNAME}.sock;
    }

}
EOF
sudo systemctl enable ${APPNAME}.socket
sudo systemctl enable ${APPNAME}.service
sudo systemctl start ${APPNAME}.socket

sudo systemctl daemon-reload
sudo systemctl restart ${APPNAME}
sudo ln -s /etc/nginx/sites-available/${APPNAME} /etc/nginx/sites-enabled
sudo systemctl restart nginx
sudo systemctl status ${APPNAME}