#!/usr/bin/env python
# encoding: utf-8
import os, sys
from relo.yapsy.IPlugin import IPlugin
import logging
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
    def pre_search(self):
        self.results = []
    def search(self, key):
        self.pre_search()
        for m in re.finditer(key, self.content):
            self.results.append(str(m.start()))
        self.post_search()
    def post_search(self):
        logging.debug("Results: " + repr(self.results))
        logging.debug("Finished with: " + self.path)

class Extension(IPlugin):
    """
    Implements external extension that can be used within relo
    """