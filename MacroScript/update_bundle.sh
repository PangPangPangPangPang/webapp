#/bin/bash
# . ./update_bundle.sh

if [ ! -d "$HOME/react-blog" ]; then
    git clone http://github.com/PangPangPangPangPang/react-blog.git $HOME
else
    cd $HOME/react-blog
    git pull
fi

rm $HOME/flask_proj/webapp/static/*
cp -r $HOME/react-blog/build/* $HOME/flask_proj/webapp/static/
cp -r $HOME/flask_proj/webapp/img/* $HOME/flask_proj/webapp/static/

. $HOME/flask_proj/webapp/MacroScript/restart.sh

