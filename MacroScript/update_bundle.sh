#/bin/bash
# . ./update_bundle.sh

if [ ! -d "$HOME/react-blog" ]; then
    git clone http://github.com/PangPangPangPangPang/react-blog.git
fi

cp $HOME/react-blog/build/bundle.js $HOME/flask-proj/webapp/static

. $HOME/flask_proj/webapp/MacroScript/restart.sh

