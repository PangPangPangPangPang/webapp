FROM ubuntu:18.04

COPY . /root/web_app
WORKDIR /root/web_app

RUN . /root/web_app/MacroScript/config_bash.sh -release

RUN apt-get update  && \
            apt-get upgrade -y  && \
            apt-get install -y git 

RUN apt-get install -y python-dev python-pip python-virtualenv nginx vim

CMD . /root/web_app/MacroScript/auto_setup.sh -release

EXPOSE 8000


