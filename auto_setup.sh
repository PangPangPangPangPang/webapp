#/bin/bash
# usage:. ./auto_setup.sh 


# prepare
cd $HOME
rm -rf flask_proj
mkdir flask_proj 

# config .bashrc(without docker)
for var in $*
do
    if [ "$var" = "-debug" ];  then
        sed -i -e "/APP_CONFIG_FILE/d" $HOME/.zshrc
        echo "export APP_CONFIG_FILE='$HOME/flask_proj/webapp/instance/env_debug.py'" >> $HOME/.zshrc
        source $HOME/.zshrc
    fi
    if [ "$var" = "-release" ];  then
        apt-get update
        apt-get install -y python-dev python-pip python-virtualenv

        sed -i -e "/APP_CONFIG_FILE/d" $HOME/.bashrc
        echo "export APP_CONFIG_FILE='$HOME/flask_proj/webapp/instance/env_release.py'" >> $HOME/.bashrc
        source $HOME/.bashrc
    fi
done

echo ----------------------------------------------------------------------------
echo ---------------------------Init virtualenv----------------------------------
echo ----------------------------------------------------------------------------

# download project
virtualenv flask_proj
cd flask_proj
git clone http://github.com/PangPangPangPangPang/webapp.git


# config nginx(ENV_TYPE is defined in Dockerfile)
if [ "$ENV_TYPE" = "release" ]; then                                                                                                                                                     
    echo ----------------------------------------------------------------------------
    echo ---------------------------Start nginx--------------------------------------
    echo ----------------------------------------------------------------------------
    apt-get install -y nginx
    cp $HOME/flask_proj/webapp/MacroScript/default /etc/nginx/sites-enabled/
    service nginx restart
fi                                                                                                                                                                                         

# update frontend bundle
echo ----------------------------------------------------------------------------
echo ---------------------------Clone repo--------------------------------------
echo ----------------------------------------------------------------------------
if [ ! -d "$HOME/react-blog" ]; then
    cd $HOME
    git clone http://github.com/PangPangPangPangPang/react-blog.git
else
    cd $HOME/react-blog
    git pull
fi

rm $HOME/flask_proj/webapp/static/*
cp -r $HOME/react-blog/build/* $HOME/flask_proj/webapp/static/
cp -r $HOME/react-blog/manual_build/* $HOME/flask_proj/webapp/static/
cp -r $HOME/flask_proj/webapp/img/* $HOME/flask_proj/webapp/static/

# enter virtualenv
cd $HOME/flask_proj/bin
. ./activate

echo ----------------------------------------------------------------------------
echo ------------------------Install python requirements-------------------------
echo ----------------------------------------------------------------------------
# install requirement
cd $HOME/flask_proj/webapp
pip2 install -r requirements.txt

echo ----------------------------------------------------------------------------
echo ------------------------------Gunicorn start--------------------------------
echo ----------------------------------------------------------------------------
# start gunicorn
pkill gunicorn
gunicorn --workers=4 --bind=127.0.0.1:8000 index:app


