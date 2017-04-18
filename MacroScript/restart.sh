#!/bin/bash
# this script must run under ./MacroScript/


cd $HOME/flask_proj/bin

. ./activate
cd ../webapp
pkill gunicorn
gunicorn --workers=4 --bind=127.0.0.1:8000 index:app
