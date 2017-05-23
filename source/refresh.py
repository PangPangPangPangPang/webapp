#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/10/2016 10:16 AM
# @Author  : Max
# @File    : refresh.py

from inter import main
import os
import json
import subprocess
from root import global_value


@main.route('/update/<regex("[a-zA-Z0-9]{32}"):key>')
def update(key):
    print key
    print global_value.SECRET_KEY
    if key != global_value.SECRET_KEY:
        return

    os.chdir(global_value.WORK_PATH + '/MacroScript')
    s = subprocess.Popen('python ./update.py', shell=True, stderr=subprocess.PIPE)
    s_ = subprocess.Popen('. restart.sh', shell=True, stderr=subprocess.PIPE)
    err = s.communicate()[1]
    err_ = s_.communicate()[1]
    ret = {}
    if not err:
        ret['pull'] = 'success'
    else:
        ret['pull'] = err
    if not err_:
        ret['restart'] = 'success'
    else:
        ret['restart'] = err_
    return json.dumps(ret)
