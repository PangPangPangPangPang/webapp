#/bin/bash
# . ./update_bundle.sh

cd $HOME
rm -rf flask_temp
mkdir flask_temp

cd flask_temp
git clone http://github.com/PangPangPangPangPang/webapp.git

cp -rf $HOME/flask_temp/webapp/resource $HOME/flask_proj/webapp/
rm -rf $HOME/flask_temp
echo -----------------------------------------------------
echo ----------update article success---------------------
echo -----------------------------------------------------


if [ ! -d "$HOME/blog_frontend" ]; then
    cd $HOME
    git clone http://github.com/PangPangPangPangPang/blog_frontend.git
else
    cd $HOME/blog_frontend
    git pull
fi

rm $HOME/flask_proj/webapp/static/*
cp -r $HOME/blog_frontend/build/* $HOME/flask_proj/webapp/static/
cp -r $HOME/flask_proj/webapp/img/* $HOME/flask_proj/webapp/static/

echo -----------------------------------------------------
echo ----------update frontend bundle success-------------
echo -----------------------------------------------------
