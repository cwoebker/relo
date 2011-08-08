#!/usr/bin/env python
# encoding: utf-8

import sys, os
from glob import glob
from interfaces import DocType
import general
from yapsy.PluginManager import PluginManager

from doctype import *

class Manager(object):
    def __init__(self, key, extList):
        self.key = key
        self.extList = extList

        self.manager = PluginManager()
        self.manager.setPluginPlaces(["doctype"])

        self.manager.locatePlugins()
        self.manager.loadPlugins()

        pluginList = []
        for plugin in self.manager.getAllPlugins():
            pluginList.append(plugin.plugin_object.meta())
        print pluginList

    def start(self, itempath):
        for plugin in self.manager.getAllPlugins():
            if plugin.plugin_object.id() == general.getFileType(itempath):
                print ("---------- "+itempath+" ----------")
                print "Using: " + plugin.plugin_object.meta()
                print "Reading File to memory..."
                plugin.plugin_object.load(itempath)
                print "Searching data..."
                plugin.plugin_object.search(self.key)
                break
            


