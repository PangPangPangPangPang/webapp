#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 01/20/2019 19:05 PM
# @Author  : Max
# @File    : update.py

from inter import main
from generate_blog_articles import generate
import os

@main.route('/update')
def update():
    os.system('../MacroScript/update_bundle.sh')
    generate()
    return 'success'
