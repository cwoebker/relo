#!/usr/bin/env python
# encoding: utf-8

import sys, os
from glob import glob
from interfaces import DocType
import general

from doctype import *

class Manager(object):
    def __init__(self, key):
        self.key = key
        plugins = 'doctype'
        if not plugins:
            return
        print "Collecting plugins..."
        files = glob(os.path.join(plugins, '*.py'))
        files.remove(plugins + '/__init__.py')
        print "Loading plugins..."
        sys.path.append(plugins) # So we can import files
        for plugin in files:
            __import__(os.path.basename(plugin).strip('.py'))
        print "Activating plugins..."
        self.plugList = DocType.implementors()
    def start(self, itempath):
        for listener in self.plugList:
            if not repr(listener).startswith('<doctype'):
                continue
            if not repr(listener).find(general.getFileType(itempath)) > 0:
                continue
            print ("---------- "+itempath+" ----------")
            print "Using: " + repr(listener)
            print "Reading File to memory..."
            listener.load(itempath)
            print "Searching data..."
            listener.search(self.key)
