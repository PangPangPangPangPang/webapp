#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 03/05/2017 11:40 AM
# @Author  : Max
# @File    : article.py


from inter import main
#  from flask import redirect, url_for, make_response
import json
#  import os
#  from generate_blog_articles import generate
from root import global_value
from flask import request


@main.route('/article')
def article():
    dic = {}
    article_id = request.args.get('id')
    if article_id:
        json_path = global_value.WORK_PATH + 'articles/' + article_id + '.md'
        art = open(json_path).read()
        dic['content'] = art
        dic['article_id'] = article_id
    else:
        dic['content'] = '文章不存在'
    ret = json.dumps(dic)
    return ret
