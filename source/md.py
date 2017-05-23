#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/10/2016 6:40 PM
# @Author  : Max
# @File    : md.py

from inter import main
from generate_blog_articles import generate


@main.route('/md')
def md():
    generate()
    return 'success'
