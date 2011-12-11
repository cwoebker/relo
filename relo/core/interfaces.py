#!/usr/bin/env python
# encoding: utf-8

from relo.yapsy.IPlugin import IPlugin
import logging
import re

reloLog = logging.getLogger('relo.log')

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
    def pre_search(self):
        self.results = []
    def search(self, key):
        self.pre_search()
        for m in re.finditer(key, self.content):
            self.results.append(str(m.start()))
        self.post_search()
    def post_search(self):
        #reloLog.debug("Results: " + repr(self.results))
        #reloLog.debug("Finished with: " + self.path)
        print "Results: " + repr(self.results)
        print "Finished with: " + self.path
class Extension(IPlugin):
    """
    Implements external extension that can be used within relo
    """

class Backend(IPlugin):
    """
    Implements external backends that can be used to store indexes and alike
    """
    name = ""
    def meta(self):
        return self.name
    def init(self):
        pass
    def check(self):
        """
        checks for old index
        """
    def load(self):
        """
        loads the current index on start
        """
        pass
    def save(self):
        """
        saves the new index to the drive
        """
        pass
    def add(self, path, modified, hash, size, type):
        """
        adds a new file to the index
        """
        pass
    def end(self):
        pass