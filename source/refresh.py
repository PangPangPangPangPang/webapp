#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/10/2016 10:16 AM
# @Author  : Max
# @File    : refresh.py

from inter import main
from webapp.index import app
import os
import json
import subprocess

@main.route('/update/<regex("[a-zA-Z0-9]{16}"):key>')
def update(key):
    os.chdir(app.config['WORK_PATH'] + '/MacroScript')
    s = subprocess.Popen('python ./update.py', shell=True, stderr=subprocess.PIPE)
    s_ = subprocess.Popen('. restart.sh', shell=True, stderr=subprocess.PIPE)
    err = s.communicate()[1]
    err_ = s_.communicate()[1]
    ret = {}
    if err is '':
        ret['pull'] = 'success'
    else:
        ret['pull'] = err
    if err_ is '':
        ret['restart'] = 'success'
    else:
        ret['restart'] = err_
    return json.dumps(ret)
