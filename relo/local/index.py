#!/usr/bin/env python
# encoding: utf-8

import os, time

from relo.core.config import conf

from relo.local import crawl
from relo.core.interfaces import Backend
from relo.yapsy.PluginManager import PluginManager
import logging
import hashlib
from progressbar import ProgressBar, RotatingMarker, Bar, Percentage, ETA, FormatLabel
#logger = logging.getLogger('relo.log')
#logging.basicConfig(level=logging.DEBUG)

from relo.core.backend import *

class CustomIndex(object):
    def __init__(self):
        pass
    def setUpBackend(self):
        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/core/backend"])
        self.manager.locatePlugins()
        print "Loading"
        self.manager.loadPlugins("<class 'relo.core.interfaces.Backend'>", ['redis'])

        for plugin in self.manager.getAllPlugins():
            self.manager.activatePluginByName(plugin.name)

        print "Plugin init done"

        for plugin in self.manager.getAllPlugins():
            print plugin.name
            if plugin.name == conf.readConfig('core.index'):
                print "Using Default: Redis"
                print plugin.plugin_object.init()
                self.db = plugin.plugin_object
    def run(self):
        pass
    def __end__(self):
        pass

class InvertedIndex(CustomIndex):
    def __init__(self, directory, hidden=False):
        self.directory = directory
        line = "| Relo Index | content | "  +  directory + " |"
        print "+" + "-" * (len(line)-2) + "+"
        print line
        print "+" + "-" * (len(line)-2) + "+"
        self.setUpBackend()
    def run(self):
        sTime = time.time()
        print "Preparing Index..."
        max = crawl.countFiles(self.directory)
        print "Indexing %d files..." % max
        pTime = time.time()
        widgets = [FormatLabel(self.directory), ' ', Percentage(), ' ', Bar('/'), ' ', RotatingMarker(), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=max).start()
        for root, subFolders, files in os.walk(self.directory):
            for file in files:
                if file.startswith('.'):
                    continue
                itempath = os.path.join(root, file)
                if os.path.islink(itempath):
                    #print "link found" + itempath
                    continue
                size = os.path.getsize(itempath)
                md5 = hashlib.md5()
                with open(itempath, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), ''):
                        md5.update(chunk)
                hash = md5.digest()
                modified = time.ctime(os.path.getmtime(itempath))
                type = crawl.getFileType(itempath)
                self.db.add(itempath, modified, hash, size, type)
                pbar.update(pbar.currval + 1)
                #print "ADD:", itempath, modified, hash, size, type
        pbar.finish()
        eTime = time.time()
        iTime = eTime - pTime
        setupTime = pTime - sTime
        tTime = eTime - sTime
        print "(Setup : %0.2fs) - (Index : %0.2fs) - (Total : %0.2fs)" % (setupTime, iTime, tTime)
    def __end__(self):
        self.db.shutdown()

class MetaIndex(CustomIndex):
    """
    Main indexing class
    """
    def __init__(self, directory, hidden=False):
        self.directory = directory
        line = "| Relo Index | meta | "  +  directory + " |"
        print "+" + "-" * (len(line)-2) + "+"
        print line
        print "+" + "-" * (len(line)-2) + "+"
        self.setUpBackend()
    def run(self):
        sTime = time.time()
        print "Preparing Index..."
        max = crawl.countFiles(self.directory)
        print "Indexing %d files..." % max
        pTime = time.time()
        widgets = [FormatLabel(self.directory), ' ', Percentage(), ' ', Bar('/'), ' ', RotatingMarker(), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=max).start()
        for root, subFolders, files in os.walk(self.directory):
            for file in files:
                if file.startswith('.'):
                    continue
                itempath = os.path.join(root, file)
                if os.path.islink(itempath):
                    #print "link found" + itempath
                    continue
                size = os.path.getsize(itempath)
                md5 = hashlib.md5()
                with open(itempath, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), ''):
                        md5.update(chunk)
                hash = md5.digest()
                modified = time.ctime(os.path.getmtime(itempath))
                type = crawl.getFileType(itempath)
                self.db.add(itempath, modified, hash, size, type)
                pbar.update(pbar.currval + 1)
                #print "ADD:", itempath, modified, hash, size, type
        pbar.finish()
        eTime = time.time()
        iTime = eTime - pTime
        setupTime = pTime - sTime
        tTime = eTime - sTime
        print "(Setup : %0.2fs) - (Index : %0.2fs) - (Total : %0.2fs)" % (setupTime, iTime, tTime)
    def __end__(self):
        self.db.shutdown()