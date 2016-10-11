#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/10/2016 6:40 PM
# @Author  : Max
# @File    : error.py

from inter import main

@main.route('/error')
def error():
    return 'errorrrrr'
