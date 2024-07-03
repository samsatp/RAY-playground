#!/bin/bash



cd /app

ARCH=`uname -m`
echo "ARCH $ARCH"


apt-get update
pip install -r /app/requirements.txt
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root