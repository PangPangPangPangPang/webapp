#!/bin/bash

path="../../bin/"
if [ ! -d "$path" ]; then
path="../bin/"
fi

cd $path
echo '.....'
pwd
echo '.....'

. activate
cd ../webapp
pkill gunicorn
gunicorn --workers=4 --bind=127.0.0.1:8000 index:app
