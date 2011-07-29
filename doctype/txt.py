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

class TXT(Plugin):
    implements = [DocType]

    def load(self, path):
        self.fobj = open(path, "r")
        self.content = ""
        for line in self.fobj:
            self.content += line
        self.fobj.close()

    def search(self, key):
        print self.content
        return "OK"