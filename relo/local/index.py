#!/usr/bin/env python
# encoding: utf-8

import os, time, re

from metaphone import dm as double_metaphone

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

##### Inverted Index Variables #####

    # Words which should not be indexed
STOP_WORDS = ("the", "of", "to", "and", "a", "in", "is", "it", "you", "that")

    # Do not index any words shorter than this
MIN_WORD_LENGTH = 3

    # Consider these characters to be punctuation (they will be replaced with spaces prior to word extraction)
PUNCTUATION_CHARS = ".,;:!?@£$%^&*()-–<>[]{}\\|/`~'\""

    # A redis key to store a list of metaphones present in this project
REDIS_KEY_METAPHONES = "id:%(project_id)s:metaphones"

    # A redis key to store a list of item IDs which have the given metaphone within the given project
REDIS_KEY_METAPHONE = "id:%(project_id)s:mp:%(metaphone)s"

class CustomIndex(object):
    def __init__(self):
        pass
    def setUpBackend(self):
        self.backendManager = PluginManager(plugin_info_ext='relo')
        self.backendManager.setPluginPlaces(["relo/core/backend"])
        self.backendManager.locatePlugins()
        print "Loading"
        self.backendManager.loadPlugins("<class 'relo.core.interfaces.Backend'>", ['redis'])

        for plugin in self.backendManager.getAllPlugins():
            self.backendManager.activatePluginByName(plugin.name)

        print "Plugin init done"

        for plugin in self.backendManager.getAllPlugins():
            print plugin.name
            if plugin.name == conf.readConfig('core.index'):
                print "Using Default: Redis"
                print plugin.plugin_object.init()
                self.db = plugin.plugin_object
    def run(self):
        pass
    def __end__(self):
        pass

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
        self.db.end()

class InvertedIndex(CustomIndex):
    def __init__(self, directory, hidden=False):
        self.directory = directory
        line = "| Relo Index | content | "  +  directory + " |"
        print "+" + "-" * (len(line)-2) + "+"
        print line
        print "+" + "-" * (len(line)-2) + "+"
        self.setUpBackend()
        self.punctuation_regex = re.compile(r"[%s]" % re.escape(PUNCTUATION_CHARS))
        super(InvertedIndex, self).__init__()
    def setUpDocType(self, extList):
        self.reloLog = logging.getLogger("relo.log")
        self.extList = extList

        self.docTypeManager = PluginManager(plugin_info_ext='relo')
        self.docTypeManager.setPluginPlaces(["relo/core/doctype"])

        self.numPlugins = self.docTypeManager.locatePlugins()
        self.docTypeManager.loadPlugins("<class 'relo.core.interfaces.DocType'>", extList=extList)

        pluginList = []
        for plugin in self.docTypeManager.getAllPlugins():
            self.docTypeManager.activatePluginByName(plugin.name)
            pluginList.append(plugin.plugin_object.meta())

    def get_words_from_text(self, text):
        """Extract a list of words to index from the given text"""
        if not text:
            return []

        text = self.punctuation_regex.sub(" ", text)
        words = text.split()

        words = [word for word in text.split() if len(word) >= MIN_WORD_LENGTH and word.lower() not in STOP_WORDS]

        return words
    def get_metaphones(self, words):
        """Get the metaphones for a given list of words"""
        metaphones = set()
        for word in words:
            metaphone = double_metaphone(unicode(word, errors='ignore'))
            print word
            print metaphone
            metaphones.add(metaphone[0].strip())
            if(metaphone[1]):
                metaphones.add(metaphone[1].strip())
        return metaphones
    def index_item(self, item, content):
        """Indexes a certain content"""

        words = self.get_words_from_text(content)

        metaphones = self.get_metaphones(words)

        for metaphone in metaphones:
            self._link_item_and_metaphone(item, metaphone)
    def _link_item_and_metaphone(self, item, metaphone):
        # Add the item to the metaphone key
        redis_key = REDIS_KEY_METAPHONE % {"project_id": self.directory, "metaphone": metaphone}
        self.db.sadd(redis_key, item)

        # Make sure we record that this project contains this metaphone
        redis_key = REDIS_KEY_METAPHONES % {"project_id": self.directory}
        self.db.sadd(redis_key, metaphone)

    def remove_project(self):
        """Remove the existing index for the project"""

        # Remove all the existing index data
        redis_key = REDIS_KEY_METAPHONES % {"project_id": self.directory}
        project_metaphones = self.db.smembers(redis_key)
        if project_metaphones is None:
            project_metaphones = []

        self.db.delete(redis_key)

        for project_metaphone in project_metaphones:
            self.db.redis.delete(REDIS_KEY_METAPHONE % {"project_id": self.directory, "metaphone": project_metaphone})

        return True
    def load(self, itempath):
        for plugin in self.docTypeManager.getAllPlugins():
            if plugin.name == crawl.getFileType(itempath).upper():
                return plugin.plugin_object.load(itempath)
        plugin = self.docTypeManager.getPluginByName("DEFAULT")
        return plugin.plugin_object.load(itempath)
    def run(self):
        sTime = time.time()
        print "Preparing Index..."
        count = crawl.countFiles(self.directory)
        size, list = crawl.recursiveListFiles(self.directory, False)
        extList = []
        for item in list:
            type = crawl.getFileType(item)
            if type not in extList:
                extList.append(type)
        del list
        self.setUpDocType(extList)
        print "Indexing %d files..." % count
        pTime = time.time()
        widgets = [FormatLabel(self.directory), ' ', Percentage(), ' ', Bar('/'), ' ', RotatingMarker(), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=count).start()
        for root, subFolders, files in os.walk(self.directory):
            for file in files:
                if file.startswith('.'):
                    continue
                itempath = os.path.join(root, file)
                if os.path.islink(itempath):
                    #print "link found" + itempath
                    continue

                content = self.load(itempath)
                print itempath
                self.index_item(itempath, content)

                pbar.update(pbar.currval + 1)
        pbar.finish()
        eTime = time.time()
        iTime = eTime - pTime
        setupTime = pTime - sTime
        tTime = eTime - sTime
        print "(Setup : %0.2fs) - (Index : %0.2fs) - (Total : %0.2fs)" % (setupTime, iTime, tTime)
    def __end__(self):
        self.db.end()


