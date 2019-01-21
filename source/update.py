#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 01/20/2019 19:05 PM
# @Author  : Max
# @File    : update.py

from inter import main
from generate_blog_articles import generate
import os
from root import global_value

@main.route('/update')
def updateArticle():
    path = global_value.WORK_PATH
    script_path = path + 'MacroScript/update_bundle.sh'
    os.system(script_path)
    generate()
    return 'success'
