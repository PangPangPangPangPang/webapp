FROM ubuntu:18.04

# release or debug
ENV ENV_TYPE release

COPY . /root/web_app
WORKDIR /root/web_app

ENV APP_CONFIG_FILE /root/flask_proj/webapp/instance/env_$ENV_TYPE.py

RUN apt-get update  && \
            apt-get install -y git  && \
            apt-get install -y python  && \
            apt-get install -y python-pip  && \
            apt-get install -y python-virtualenv  && \
            apt-get install -y nginx  && \
            apt-get install -y vim 

EXPOSE 80

CMD ["sh", "/root/web_app/auto_setup.sh", "-$ENV_TYPE"] 

