#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : May 20, 2017
# @Author  : Max
# @File    : inter.py


from inter import main
#  from root import global_value
from flask import request
import uuid
import json


namespace = 'chat_namespace'

li = {}


class Pair(object):
    __slots__ = {
            'user_one', 'user_two'
            }

    def __init__(self, user_one=None, user_two=None):
        self.user_one = user_one
        self.user_two = user_two


def generateId(str):
    return uuid.uuid5(uuid.NAMESPACE_DNS, str.decode().encode('utf-8'))


def generateAndAddChat(obj, ws):
    if obj['action'] != 'register':
        return False

    k = generateId(obj['from'] + obj['to'])
    k = str(k)
    k_ = generateId(obj['to'] + obj['from'])
    k_ = str(k_)
    if not li.get(k) and not li.get(k_):
        p = Pair(user_one=ws)
        li[k] = p
        return True
    elif li.get(k):
        chat = li.get(k)
        u1 = chat.user_one
        if u1.closed:
            chat.user_one = ws
            chat.user_two = None
        else:
            if not chat.user_two:
                chat.user_two = ws
                return True
    elif li.get(k_):
        chat = li.get(k_)
        if not chat.user_two:
            chat.user_two = ws
            return True
    return False


def getChat(obj):
    k = generateId(obj['from'] + obj['to'])
    k = str(k)
    k_ = generateId(obj['to'] + obj['from'])
    k_ = str(k_)
    if li.get(k):
        return li.get(k)
    elif li.get(k_):
        return li.get(k_)
    else:
        return None


@main.route('/chat')
def chat():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        if ws is None:
            return 'failure'
            #  abort(404)
        else:
            while True:
                if not ws.closed:
                    message = ws.receive()
                    print message
                    message_obj = json.loads(message)
                    # generate chatroom
                    isGenerateSuccess = generateAndAddChat(message_obj, ws)
                    if message_obj['action'] == 'register':
                        if isGenerateSuccess:
                            print 'register success'
                            ret = {'message': 'Register success!'}
                            ws.send(json.dumps(ret, indent=1))
                        continue
                    chat = getChat(message_obj)
                    if ws is chat.user_one and chat.user_two \
                            and not chat.user_two.closed:
                        chat.user_two.send(message)
                    elif ws is chat.user_two and chat.user_one \
                            and not chat.user_one.closed:
                        chat.user_one.send(message)
                    else:
                        ret = {'message': 'Your friend is not online!'}
                        ws.send(json.dumps(ret, indent=1))
                else:
                    print 'closed'
