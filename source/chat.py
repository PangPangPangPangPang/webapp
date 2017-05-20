#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : May 20, 2017
# @Author  : Max
# @File    : inter.py


from inter import main
#  from root import global_value
from flask import request


@main.route('/chat')
def chat():
    print request.environ['wsgi.websocket']
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        if ws is None:
            abort(404)
        else:
            while True:
                if not ws.closed:
                    message = ws.receive()
                    ws.send('wooooo')

