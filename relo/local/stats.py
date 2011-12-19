#!/usr/bin/env python
# encoding: utf-8

import os, time

from relo.core.config import conf
from relo.core.log import logger

from relo.core.interfaces import Statistic
from relo.yapsy.PluginManager import PluginManager
from relo.local.statistics import *


class Stats(object):
    """
    Main Stats class
    """
    def __init__(self, directory, module, hidden=False):
        self.directory = directory
        self.module = module

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/local/statistics"])
        self.manager.locatePlugins()
        self.manager.loadPlugins("<class 'relo.core.interfaces.Statistics'>", ['disk'])
        print "Plugin init done"
    def check(self):
        for plugin in self.manager.getAllPlugins():
            if self.module.upper() == plugin.name:
                return True
        return False
    def list(self):
        """
        Lists all available modules.
        """
        print "Available Statistic plugins:"

        for plugin in self.manager.getAllPlugins():
            print "    - " + plugin.name
    def go(self):
        for plugin in self.manager.getAllPlugins():
            self.manager.activatePluginByName(plugin.name)
            print plugin.name
            if plugin.name == self.module.upper():
                print "Found module"
                self.module = plugin.plugin_object
        self.module.init(self.directory)
        self.module.execute()
        self.module.end()