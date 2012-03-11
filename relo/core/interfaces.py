#!/usr/bin/env python
# encoding: utf-8

from relo.yapsy.IPlugin import IPlugin
import logging

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


class Statistic(ReloPlugin):
    """
    Plugin for modules that can use the index or pull information directly from the filesystem and analyze it
    """
    name = ""

    def init(self, directory):
        pass

    def execute(self):
        pass

    def end(self):
        pass
