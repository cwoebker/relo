#!/usr/bin/env python
# encoding: utf-8

import sys, os
from glob import glob
from interfaces import DocType

from doctype import *

class Manager(object):
    def __init__(self, key):
        self.key = key
        pass
    def start(self, itempath):
        plugins = 'doctype'
        if plugins:
            files = glob(os.path.join(plugins, '*.py'))
            print files
            files.remove(plugins + '/__init__.py')
            sys.path.append(plugins) # So we can import files
            for plugin in files:
                __import__(os.path.basename(plugin).strip('.py'))
        plugList = DocType.implementors()
        for listener in plugList:
            if not repr(listener).startswith('<doctype'):
                continue
            listener.load(itempath)
            listener.search(self.key)
            print repr(listener)
