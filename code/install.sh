#!/bin/bash 

echo 'Installing requirements..'

pip3 install -r ../requirements.txt

chmod +x panoptes.py

mkdir /var/log/panoptes/
mkdir /etc/panoptes/

echo 'Config.py created'

cp config.example config.py
