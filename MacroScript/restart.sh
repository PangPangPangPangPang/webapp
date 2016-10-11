#!/bin/bash

cd ../../bin/
. activate
cd ../webapp
pkill gunicorn
gunicorn --workers=4 --bind=127.0.0.1:8000 index:app

