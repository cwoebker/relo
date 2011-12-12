#!/usr/bin/env python
# encoding: utf-8

import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.config import conf

from relo.core.interfaces import Statistic

# For Index
from relo.core.interfaces import Backend
from relo.yapsy.PluginManager import PluginManager

class DISKSPACE(Statistic):
    name = "diskspace"
    def init(self, directory):
        self.directory = directory

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/core/backend"])
        self.manager.locatePlugins()
        print "Loading"
        self.manager.loadPlugins("<class 'relo.core.interfaces.Backend'>", ['redis'])

        pluginList = []
        for plugin in self.manager.getAllPlugins():
            self.manager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())

        print "Plugin init done"

        for plugin in self.manager.getAllPlugins():
            print plugin.name
            if plugin.name == conf.readConfig('core.index'):
                print "Using Default: Redis"
                print plugin.plugin_object.init()
                self.backend = plugin.plugin_object
    def execute(self):
        files = self.backend.find(os.path.abspath(self.directory))
        print files
        print len(files)
    def end(self):
        print "end"