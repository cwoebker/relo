#!/usr/bin/env python
# encoding: utf-8

import sys, os
from glob import glob
from interfaces import DocType
import general

from doctype import *

class Manager(object):
    def __init__(self, key, extList):
        self.key = key
        self.extList = extList
        plugins = 'doctype'
        print "Collecting plugins..."
        files = glob(os.path.join(plugins, '*.py'))
        files.remove(plugins + '/__init__.py')
        print "Filtering plugins..."
        removeList = []
        for item in files:
            ext = os.path.basename(item)
            ext = ext.rstrip('.py')
            if ext not in extList:
                removeList.append(item)
        files = list(set(files) - set(removeList))
        print "Loading plugins..."
        sys.path.append(plugins) # So we can import files
        for plugin in files:
            __import__(os.path.basename(plugin).strip('.py'))
        print "Loaded plugins: " + repr(files)

        print "Activating plugins..."
        self.plugList = DocType.implementors()
        print self.plugList
        for plug in self.plugList:
            print 'ping'
            print repr(plug)
            for ext in extList:
                if not repr(plug).find(ext) > 0:
                    self.plugList.remove(plug)
        print self.plugList
        for plug in self.plugList:
            print 'ping'
            print repr(plug)

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
            break


