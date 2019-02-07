#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

import pymongo

'''
class MongodbConn(object):
    def __init__(self):
        self.Mongodb_IP = "10.6.0.144"
        self.Port = 27017

    def Client(self, dbname, table):
        client = pymongo.MongoClient(self.Mongodb_IP, self.Port)
        db = client.dbname
        collection = db.table
        return collection
'''

Mongodb_IP = "10.6.0.144"
Port = 27017

def Client():
    client = pymongo.MongoClient(Mongodb_IP, Port)
    return client

# db = client.genieacs
# collection = db.devices
# task_collection = db.tasks