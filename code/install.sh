#!/bin/bash 

echo 'Installing requirements..'

pip3 install -r ../requirements.txt

chmod +x panoptes.py

echo 'Config.py created'

cp config.example config.py
