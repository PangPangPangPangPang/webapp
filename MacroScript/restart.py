import os

# os.system('. /root/flask_proj/bin/activate')

os.system('cd /root/flask_proj/webapp')
# os.system('pkill gunicorn')
os.system('gunicorn --workers=4 --bind=127.0.0.1:8000 index:app')
