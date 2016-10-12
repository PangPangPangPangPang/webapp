#,gD8]y+FGbNJ-A@{
#45.32.31.64
from flask import Flask
from webapp.source import AppDelegate

app = Flask(__name__)
app.config.from_object(__name__)

root = AppDelegate(app)
root.register()

if __name__ == '__main__':
    app.run()
