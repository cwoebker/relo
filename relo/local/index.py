#!/usr/bin/env python
# encoding: utf-8

import os
from relo.local import crawl
from relo.core.interfaces import Backend
from relo.yapsy.PluginManager import PluginManager
import logging
import hashlib
#logger = logging.getLogger('relo.log')
logging.basicConfig(level=logging.DEBUG)

from relo.core.backend import *

class Index(object):
    def __init__(self, directory, hidden=False, content=False):
        """
        Main indexing class
        """
        self.directory = directory
        f = lambda content: content==True and 'content' or 'meta'
        print "-------------------------------------------------"
        print "Relo Index |",directory,"|", f(content)
        print "-------------------------------------------------"

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/core/backend"])
        self.manager.locatePlugins()
        print "Loading"
        self.manager.loadPlugins("<class 'relo.core.interfaces.Backend'>", ['redis']) #

        pluginList = []
        for plugin in self.manager.getAllPlugins():
            self.manager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())

        print "Plugin init done"

        for plugin in self.manager.getAllPlugins():
            print plugin.name
            if plugin.name == "REDISDB":
                print "Using Default: Redis"
                print plugin.plugin_object.init()
                self.backend = plugin.plugin_object

    def list(self):
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
                type = crawl.getFileType(itempath)
                self.backend.add(itempath, hash, size, type)
                print "ADD:", itempath, hash, size, type

    def go(self):
        pass
    def end(self):
        self.backend.shutdown()