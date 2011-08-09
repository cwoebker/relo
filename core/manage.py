#!/usr/bin/env python
# encoding: utf-8

#import sys, os
from interfaces import DocType
import core
from yapsy.PluginManager import PluginManager

from doctype import *

import logging
logging.basicConfig(level=logging.DEBUG)

class Manager(object):
    def __init__(self, key, extList):
        self.key = key
        self.extList = extList

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["doctype"])

        self.manager.locatePlugins()
        self.manager.loadPlugins("<class 'core.interfaces.DocType'>")

        pluginList = []
        for plugin in self.manager.getAllPlugins():
            self.manager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())
        print pluginList

    def start(self, itempath):
        print itempath
        for plugin in self.manager.getAllPlugins():
            if plugin.name == core.getFileType(itempath).upper():
                print ("---------- "+itempath+" ----------")
                print "Using: " + plugin.plugin_object.meta()
                print "Reading File to memory..."
                plugin.plugin_object.load(itempath)
                print "Searching data..."
                plugin.plugin_object.search(self.key)
                break


