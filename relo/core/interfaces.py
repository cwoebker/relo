#!/usr/bin/env python
# encoding: utf-8

from relo.yapsy.IPlugin import IPlugin
import logging
import re

reloLog = logging.getLogger('relo.log')

class ReloPlugin(IPlugin):
    """
    A custom ReloPlugin based of the standard IPlugin provided by yapsy

    (not implemented yet)
    """
    name = ""
    def meta(self):
        return self.name

class DocType(ReloPlugin):
    """""
    Implements different type of docs
    """""
    def load(self, path):
        self.path = path
        self.fobj = open(path, "r")
        self.content = ""
        for line in self.fobj:
            self.content += line
        self.fobj.close()
        return self.content

class Extension(IPlugin):
    """
    Implements external extension that can be used within relo
    """

class Backend(IPlugin):
    """
    Implements external backends that can be used to store indexes and alike
    """
    name = ""
    def meta(self):
        return self.name
    def init(self):
        pass
    def check(self):
        """
        checks for old index
        """
    def load(self):
        """
        loads the current index on start
        """
        pass
    def save(self):
        """
        saves the new index to the drive
        """
        pass
    def addMeta(self, path, modified, hash, size, type):
        """
        adds a new file to the index
        """
        pass
    def end(self):
        pass

class Statistic(IPlugin):
    """
    Plugin for modules that can use the index or pull information directly from the filesystem and analyze it
    """
    name = ""
    def meta(self):
        return self.name
    def init(self, directory):
        pass
    def execute(self):
        pass
    def end(self):
        pass