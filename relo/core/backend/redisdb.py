#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import redis

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.interfaces import Backend

class REDISDB(Backend):
    name = "redis"
    expiretime = 60*60*24*7
    def init(self):
        print "Connecting to Redis"
        self.db = redis.StrictRedis(host='localhost', port=6379, db=11)
    def check(self):
        print "check not needed with redis"
    def load(self):
        print "Redis auto loads"
    def save(self):
        self.db.save()
    def add(self, path, modified, hash, size, type):
        pipe = self.db.pipeline()
        pipe.hmset(path, dict(modified=modified, hash=hash, size=size, type=type)).expire(path, self.expiretime).execute()
        del pipe
    def find(self, key):
        return self.db.keys(pattern='*'+key+'*')
    def end(self):
        self.db.shutdown()