#!/usr/bin/env python
# encoding: utf-8

import os
from relo.core.interfaces import Backend
from relo.yapsy.PluginManager import PluginManager
import logging
#logger = logging.getLogger('relo.log')
logging.basicConfig(level=logging.DEBUG)

from relo.core.backend import *

class Index:
    def __init__(self, directory, hidden=False, content=False):
        """
        Main indexing class
        """
        f = lambda content: content==True and 'content' or 'meta'
        print "-------------------------------------------------"
        print "Relo Index |",directory,"|", f(content)
        print "-------------------------------------------------"

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/core/backend"])
        self.manager.locatePlugins()
        print "Loading"
        self.manager.loadPlugins("jdhfslkasjdhfkjsdhfjasjkhdfk") #"<class 'relo.core.interfaces.Backend'>"

        pluginList = []
        for plugin in self.manager.getAllPlugins():
            print plugin.name
            self.manager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())

        print "Plugin init done"

        for plugin in self.manager.getAllPlugins():
            print plugin.name
            if plugin.name == "redis_db":
                print "Using Default: Redis"
                print plugin.plugin_object.init()

    def list(self):
        pass
    def go(self):
        pass