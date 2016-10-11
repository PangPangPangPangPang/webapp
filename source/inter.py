#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/10/2016 6:32 PM
# @Author  : Max
# @File    : inter.py

from flask import Blueprint

main = Blueprint('inter', __name__)
from . import error