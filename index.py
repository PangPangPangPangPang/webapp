from flask import Flask
from source import AppDelegate, Mongo_db
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
app.config.from_object(__name__)

root = AppDelegate(app)
root.register()

# Init Article list
#  generate()

db = Mongo_db()
#  try:
    #  db.addUser({
        #  'name': 'wangyefeng'
        #  })
#  except BaseException, exception:
    #  print exception


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
