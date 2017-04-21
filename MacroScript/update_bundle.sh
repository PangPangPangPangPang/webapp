#/bin/bash
# . ./update_bundle.sh

if [ ! -d "$HOME/react-blog" ]; then
    git clone http://github.com/PangPangPangPangPang/react-blog.git $HOME
fi

cd $HOME/react-blog
git pull

cp $HOME/react-blog/build/bundle.js $HOME/flask_proj/webapp/static/bundle.js

. $HOME/flask_proj/webapp/MacroScript/restart.sh

