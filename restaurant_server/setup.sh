#!/usr/bin/sh
# TODO use something more lightweight than apache
apt install apache2 sshd
DIR=/usr/local/yacwa/

mkdir -p $DIR
cp ./sick_updater.py $DIR
cp ./corona_fileupdater.py $DIR

cat >> /etc/ssh/sshd_config <<EOF
Match User gesundheitsamt
       X11Forwarding no
       AllowTcpForwarding no
       PermitTTY no
       ForceCommand $DIR/sick_updater.py
EOF
useradd --shell $DIR/sick_updater.py --home-dir $DIR yacwa
mkdir -p $DIR/.ssh
cp ./id_yacwa.pub $DIR/.ssh/authorized_keys
usermod -aG www-data yacwa
service sshd reload
