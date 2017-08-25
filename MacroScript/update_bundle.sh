#/bin/bash
# . ./update_bundle.sh

if [ ! -d "$HOME/react-blog" ]; then
    cd $HOME
    git clone http://github.com/PangPangPangPangPang/react-blog.git
else
    cd $HOME/react-blog
    git pull
fi

rm $HOME/flask_proj/webapp/static/*
cp -r $HOME/react-blog/build/* $HOME/flask_proj/webapp/static/
cp -r $HOME/react-blog/index.html $HOME/flask_proj/webapp/static/
cp -r $HOME/flask_proj/webapp/img/* $HOME/flask_proj/webapp/static/

