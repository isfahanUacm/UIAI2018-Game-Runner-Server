#!/usr/bin/env bash

git pull
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
sudo rm -rf /var/lib/lxc/base2/rootfs/opt/uiai2018/game_runner
sudo cp -vr game_runner /var/lib/lxc/base2/rootfs/opt/uiai2018/
sudo rm -rf /opt/uiai2018/game_runner
sudo cp -vr game_runner /opt/uiai2018/
sudo service uwsgi restart
sudo service nginx restart