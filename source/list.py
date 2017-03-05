#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 03/05/2017 11:40 AM
# @Author  : Max
# @File    : list.py


from inter import main
#  from flask import redirect, url_for, make_response
#  import json
#  import os
#  from generate_blog_articles import generate
from root import global_value

@main.route('/list')
def article_list():
    json_path = global_value.WORK_PATH + 'articles/list.json'
    ret = open(json_path).read()
    return ret
