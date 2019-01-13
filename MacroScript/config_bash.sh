#/bin/bash
# usage:. ./config_bash.sh -release

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
