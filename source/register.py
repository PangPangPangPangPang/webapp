#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-05-24 14:48
# @Author  : Max
# @File    : register.py
from inter import main
from flask import request
import pprint
from source import Mongo_db
import json


@main.route('/register')
def register():
    ret = {}
    register_args = request.args.to_dict()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(register_args)
    db = Mongo_db()
    try:
        _id = db.addUser(register_args)
    except BaseException, post:
        _id = post[1]['_id']
        ret['message'] = 'Already registered!'
        ret['statusCode'] = 99
        ret['userId'] = str(_id)
        return json.dumps(ret)
    ret['message'] = ' Aegister success!'
    ret['statusCode'] = 1
    ret['userId'] = str(_id)
    return json.dumps(ret)
