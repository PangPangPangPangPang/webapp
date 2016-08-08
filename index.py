from flask import Flask
from source import AppDelegate

app = Flask(__name__)

root = AppDelegate(app)
root.register()

if __name__ == '__main__':
    app.run()
