#!/usr/bin/env python
# encoding: utf-8
import re

from relo import core
# from relo.core.interfaces import DocType
from relo.yapsy.PluginManager import PluginManager
from relo.local import util
from relo.core import doctype
from relo.core import config
from relo.core.config import conf
from relo.core.log import logger
import os, time
from progressbar import ProgressBar, RotatingMarker, Bar, ReverseBar, \
                        Percentage
from metaphone import dm as double_metaphone

# from relo.core.doctype import *

def checkIndex(path):
    absolute = os.path.abspath(path)
    def setUpBackend():
        backendManager = PluginManager(plugin_info_ext='relo')
        backendManager.setPluginPlaces(["relo/core/backend"])
        backendManager.locatePlugins()
        backendManager.loadPlugins("<class 'relo.core.interfaces.Backend'>", ['redis'])

        for plugin in backendManager.getAllPlugins():
            backendManager.activatePluginByName(plugin.name)

        for plugin in backendManager.getAllPlugins():
            if plugin.name == conf.readConfig('core.index'):
                db = plugin.plugin_object
                db.init()
                return db
    db = setUpBackend()
    project_list = db.listProjects(config.REDIS_KEY_PROJECTS)
    for project in project_list:
        if project[0] == absolute:
            return project[1:]
    return None

def fileNameSearch(fileList, key):
    for itempath in fileList:
        item = os.path.basename(itempath)
        if not item.find(key) == -1:
            logger.log("Found: " + itempath)

class CustomSearch(object):
    def __init__(self):
        pass

class IndexSearch(CustomSearch):
    def __init__(self, directory, key):
        self.directory = directory
        self.key = key
        self.setUpBackend()
        self.results = []
    def setUpBackend(self):
        self.backendManager = PluginManager(plugin_info_ext='relo')
        self.backendManager.setPluginPlaces(["relo/core/backend"])
        self.backendManager.locatePlugins()
        self.backendManager.loadPlugins("<class 'relo.core.interfaces.Backend'>", ['redis'])

        for plugin in self.backendManager.getAllPlugins():
            self.backendManager.activatePluginByName(plugin.name)

        for plugin in self.backendManager.getAllPlugins():
            if plugin.name == conf.readConfig('core.index'):
                self.db = plugin.plugin_object
                self.db.init()
    def loadFiles(self):
        return self.db.getSet(config.REDIS_KEY_DOCUMENTS % {"project_id": self.directory})
    def loadMetaphones(self):
        return self.db.getSet(config.REDIS_KEY_METAPHONES % {"project_id": self.directory})
    def nameSearch(self):
        files = self.loadFiles()
        for file in files:
            item = os.path.basename(file)
            if not item.find(self.key) == -1:
                self.results.append(file)
    def contentSearch(self):
        metaphones = self.loadMetaphones() ## do part of search in redis itself in the future so we dont hae to laod everything, keys *mp*
        # or just try to load metaphone and see what you get
        key_mps = double_metaphone(unicode(self.key, errors='ignore'))
        for mp in metaphones: # filter, map and reduce should help here in future
            for key_mp in key_mps:
                if key_mp == mp:
                    self.results.extend(self.db.getSet(config.REDIS_KEY_METAPHONE % {"project_id": self.directory, "metaphone":key_mp}))
    def printResult(self):
        if len(self.results) == 0:
            logger.item("No results found")
        else:
            for item in self.results:
                logger.item(item)

class Search(CustomSearch):
    def __init__(self, info=False, debug=False, all=False, hidden=False, filelog=False, content=False, recursive=False,
                 doctype=None, directory='./', key=''):
        """
        Main Relo class
        """
        self.name = "relo"
        self.info = info
        self.debug = debug
        self.filelog = filelog
        self.all = all
        self.hidden = hidden
        self.recursive = recursive
        self.doctype = doctype
        self.dir = directory
        self.key = key

        if content:
            self.type = "content Search"
        else:
            self.type = "fileName Search"

        logger.info("Relo: version %s" % core.config.get_version())
        if self.info:
            logger.info("Mode: Info")
        elif self.debug:
            logger.info("Mode: Debug")
        else:
            logger.info("Mode: Normal")
        logger.info("All Files: " + str(bool(self.all)))
        if self.doctype is None:
            logger.info("Special DocType: None")
        else:
            logger.info("Special DocType: " + self.doctype)
        logger.info("Hidden Files: " + str(bool(self.hidden)))
        logger.info("Recursive: " + str(bool(self.recursive)))
        logger.info("Search Type: " + self.type)
        logger.info("Directory: " + self.dir)
        logger.info("Searching for: " + self.key)

        self.filteredList = []
        self.extList = []
        self.total_size = 0
        self.fileList = []

        logger.head("Relo Search | " + self.dir + " | '" + self.key + "'")

        #Main Progress Bar
        self.mainWidgets = ['Searching: ', Percentage(), ' ', Bar('>'),
                   ' ', RotatingMarker()]
    def list(self):
        widgets = ["Listing directory content... ",
                   Bar('>'), ' ', RotatingMarker(), ' ', ReverseBar('<')]
        pbar = ProgressBar(widgets=widgets, maxval=100).start()
        pbar.update(0)
        time.sleep(0.5)
        if self.recursive:
            logger.debug("Listing directory content recursively...")
            pbar.update(20)
            time.sleep(1)
            self.total_size, self.fileList = util.recursiveListFiles(self.dir, self.hidden)
        else:
            logger.debug("Listing directory content...")
            pbar.update(20)
            time.sleep(1)
            self.total_size, self.fileList = util.listFiles(self.dir, self.hidden)
        pbar.update(100)
        pbar.finish()
        logger.debug("Supported File Types: " + repr(doctype.__all__))
        logger.info("Size of directory - %d" % self.total_size)

    def filter(self):
        if self.all:
            logger.info("No filter applied")
            self.filteredList = self.fileList
        elif not self.doctype is None:
            logger.log("Selecting DocType files...")
            self.filteredList = util.filterDocType(self.fileList, self.doctype)
        else:
            logger.log("Filtering file types...")
            self.filteredList = util.filterList(self.fileList)
        for itempath in self.filteredList:
            item = util.getFileType(itempath)
            if item not in self.extList:
                self.extList.append(item)

    def start(self):
        if len(self.filteredList) == 0:
            logger.error("No files in range.")
            return 0
        self.pbar = ProgressBar(widgets=self.mainWidgets, maxval=len(self.filteredList)).start()
        if 'content' in self.type:
            self.startContent()
        else:
            self.startName()
        self.pbar.finish()
        self.printResults()
    def startName(self):
        fileNameSearch(self.fileList, self.key)
    def startContent(self):
        self.setUpDocType(self.extList)
        i = 0
        self.results = {}
        for item in self.filteredList:
            self.pbar.update(i)
            content = self.load(item)
            self.search(content, item)
            i += 1
            self.pbar.update(i)
    def search(self, string, item):
        found = []
        for m in re.finditer(self.key, string):
            found.append(str(m.start()))
        self.results[item] = found
    def printResults(self):
        logger.head("Search Results | " + self.dir + " | '" + self.key + "'")
        for key, value in self.results.iteritems():
            if not value:
                continue
            logger.item(key)
            logger.subitem(repr(value))
    def setUpDocType(self, extList):
        self.extList = extList

        self.manager = PluginManager(plugin_info_ext='relo')
        self.manager.setPluginPlaces(["relo/core/doctype"])

        self.numPlugins = self.manager.locatePlugins()
        self.manager.loadPlugins("<class 'relo.core.interfaces.DocType'>", extList=extList)

        pluginList = []
        for plugin in self.manager.getAllPlugins():
            self.manager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())
            #print pluginList

    def load(self, itempath):
        for plugin in self.manager.getAllPlugins():
            if plugin.name == util.getFileType(itempath).upper():
                return plugin.plugin_object.load(itempath)
        plugin = self.manager.getPluginByName("DEFAULT")
        return plugin.plugin_object.load(itempath)