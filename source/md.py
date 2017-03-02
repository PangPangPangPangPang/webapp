#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/10/2016 6:40 PM
# @Author  : Max
# @File    : md.py

from inter import main
# from flask import redirect, url_for
import json

@main.route('/main')
def main():
    dic = {}
    dic['content'] = open('../resource/Auto Layout中的VFL使用教程（译）.md', 'rb').read()
    ret = json.dumps(dic, indent=1)
    return ret
