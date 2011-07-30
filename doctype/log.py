#!/usr/bin/env python
# encoding: utf-8
import sys
import os

__author__ = 'cwoebker'

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from general.interfaces import DocType
from plugnplay import Plugin, man

import re

class LOG(Plugin):
    implements = [DocType]

    def load(self, path):
        self.path = path
        self.fobj = open(path, "r")
        self.content = ""
        for line in self.fobj:
            self.content += line
        self.fobj.close()

    def search(self, key):
        if self.content.find(key) > 0:
            print "Match in", self.path
            for m in re.finditer(key, self.content):
                print m.start()
                
        return "OK"