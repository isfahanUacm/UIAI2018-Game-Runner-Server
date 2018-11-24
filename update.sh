#!/usr/bin/env bash

git pull
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
sudo rm -rf /var/lib/lxc/uiai2018base/rootfs/opt/uiai2018/game_runner
sudo cp -vr game_runner /var/lib/lxc/uiai2018base/rootfs/opt/uiai2018/
sudo service uwsgi restart
sudo service nginx restart