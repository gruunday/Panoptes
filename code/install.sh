#!/bin/bash 

echo "Installing requirements.."

pip3 install --upgrade setuptools
pip3 install -r ../requirements.txt

chmod +x panoptes.py

if [ ! -d /var/log/panoptes/ ]; then
    mkdir /var/log/panoptes/
fi

if [ ! -d /etc/panoptes/ ]; then
    mkdir /etc/panoptes/
fi

if [ ! -f config.json ]; then
    echo "Config.py created"
    cp config.example config.json
else
    echo "Using old config"
fi
