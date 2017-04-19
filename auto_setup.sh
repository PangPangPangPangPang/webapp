#/bin/bash
# usage:. ./auto_setup.sh -debug

cd $HOME
rm -rf flask_proj
mkdir flask_proj 

# config .bashrc
for var in $*
do
    if [ "$var" = "-debug" ];  then
        sed -i -e "/APP_CONFIG_FILE/d" $HOME/.zshrc
        echo "export APP_CONFIG_FILE='$HOME/flask_proj/webapp/instance/env_debug.py'" >> $HOME/.zshrc
        source $HOME/.zshrc
    fi
    if [ "$var" = "-release" ];  then
        sed -i -e "/APP_CONFIG_FILE/d" $HOME/.bashrc
        echo "export APP_CONFIG_FILE='$HOME/flask_proj/webapp/instance/env_release.py'" >> $HOME/.bashrc
        source $HOME/.bashrc
    fi
done

# download project
virtualenv flask_proj
cd flask_proj
# cp -r $HOME/webapp webapp
git clone http://github.com/PangPangPangPangPang/webapp.git

# enter virtualenv
cd $HOME/flask_proj/bin
. ./activate

cd $HOME/flask_proj/webapp
pip install -r requirements.txt

pkill gunicorn
gunicorn --workers=4 --bind=127.0.0.1:8000 index:app


