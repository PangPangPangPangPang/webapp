import os

os.system('pkill gunicorn')
os.system('gunicorn --workers=4 --bind=127.0.0.1:8000 ../index:app')