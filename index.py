from flask import Flask
from source import AppDelegate
from flask_socketio import SocketIO
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)

root = AppDelegate(app)
root.register()


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #  socketio.run(app)
    #  app.run()
