#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-05-23 16:23
# @Author  : Max
# @File    : singleton.py


def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance
