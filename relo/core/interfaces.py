#!/usr/bin/env python
# encoding: utf-8
import os, sys
from relo.yapsy.IPlugin import IPlugin

import re

class DocType(IPlugin):
    """""
    Implements different type of docs
    """""
    name = ""
    def meta(self):
        return self.name
    def load(self, path):
        self.path = path
        self.fobj = open(path, "r")
        self.content = ""
        for line in self.fobj:
            self.content += line
        self.fobj.close()
    def search(self, key):
        if not (re.search(key, self.content) == None):
            for m in re.finditer(key, self.content):
                print "Found at position: " + str(m.start())
        else:
            print "Nothing found"

        print "Finished with: " + self.path

class Extension(IPlugin):
    """
    Implements external extension that can be used within relo
    """