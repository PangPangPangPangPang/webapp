#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/10/2016 6:40 PM
# @Author  : Max
# @File    : error.py

from inter import main
# from flask import redirect, url_for
import json


@main.route('/error')
def error():
    dic = {}
    dic['user'] = 'wang'
    arr = []
    dic['friends'] = arr
    arr.append({'name': 'songyue'})
    arr.append({'name': 'www'})
    arr.append({'name': 'bbb'})
    arr.append({'name': 'ccc'})
    ret = json.dumps(dic, indent=1)
    print ret
    return ret
