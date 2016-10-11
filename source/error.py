#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/10/2016 6:40 PM
# @Author  : Max
# @File    : error.py

from inter import main
from flask import redirect, url_for

@main.route('/error')
def error():
    print url_for('.index')
    return url_for('.index')
