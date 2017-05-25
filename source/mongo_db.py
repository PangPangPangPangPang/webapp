#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-05-23 16:00
# @Author  : Max
# @File    : mongo_db.py
from pymongo import MongoClient
from util import singleton


@singleton
class Mongo_db:
    __slot__ = {
            'client',
            'db'
            }

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.db

# users db user 'name' as unique key.
    def addUser(self, obj):
        post = self.getUser(obj['name'])
        if post is not None:
            raise Exception('Already Exist', post)
        userID = self.db.users.insert_one(obj).inserted_id
        return userID

    def getUser(self, name):
        post = self.db.users.find_one({'name': name})
        return post

    def updataUser(self, obj, obj_id):
        pass
