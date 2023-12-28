#! /bin/bash
su root
apt install -y curl 
curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-7.17.15-amd64.deb
dpkg -i apm-server-7.17.15-amd64.deb
mv apm-server.yml /etc/apm-server/apm-server.yml
chmod 755 /etc/apm-server/apm-server.yml
service apm-server start
echo "Done ..."
