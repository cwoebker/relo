#!/usr/bin/env python
# encoding: utf-8

#import sys, os
from relo.core.interfaces import DocType
from relo.local import crawl
from relo.yapsy.PluginManager import PluginManager
import logging
logging.basicConfig(level=logging.DEBUG)
import pdb


from relo.core.doctype import *

class Manager(object):
    def __init__(self, key, extList):
        self.reloLog = logging.getLogger("relo.log")
        self.key = key
        self.extList = extList

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/core/doctype"])

        self.numPlugins = self.manager.locatePlugins()
        #print "Found %d plugins." % self.numPlugins
        #self.manager.loadPlugins("<class 'core.interfaces.DocType'>")
        self.manager.loadPlugins("<class 'relo.core.interfaces.DocType'>", extList=extList)
        
        pluginList = []
        for plugin in self.manager.getAllPlugins():
            print plugin.name
            self.manager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())
        #print pluginList
        self.reloLog.info("Manager initialized...")

    def start(self, itempath):
        for plugin in self.manager.getAllPlugins():
            if plugin.name == crawl.getFileType(itempath).upper():
                self.reloLog.debug(("---------- "+itempath+" ----------"))
                self.reloLog.debug("Using: " + plugin.plugin_object.meta())
                self.reloLog.debug("Reading File to memory...")
                plugin.plugin_object.load(itempath)
                self.reloLog.debug("Searching data...")
                plugin.plugin_object.search(self.key)
                return
        plugin = self.manager.getPluginByName("DEFAULT")
        self.reloLog.debug(("---------- "+itempath+" ----------"))
        self.reloLog.debug("Using: " + plugin.plugin_object.meta())
        self.reloLog.debug("Reading File to memory...")
        plugin.plugin_object.load(itempath)
        self.reloLog.debug("Searching data...")
        plugin.plugin_object.search(self.key)


