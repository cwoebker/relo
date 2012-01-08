#!/usr/bin/env python
# encoding: utf-8

import string, sys, os
from os.path import *

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.config import conf
from relo.local import util

from relo.core.interfaces import Statistic

# For Index
from relo.core.interfaces import Backend
from relo.yapsy.PluginManager import PluginManager

class DISKSPACE(Statistic):
    name = "diskspace"
    def init(self, directory):
        self.directory = directory

        # Options
        self.cumPercent = 80
        self.topNOption = 'n'
        self.maxDepth = 2
        self.showFiles = False
        self.indentSize = 4
        self.followLinks = False
        self.topN = 5
        self.percent = 10
        self.units = 'k'
    def getIndentStr(self, depth, isDir):
        s = ''
        for i in range(depth):
            if isDir and i == depth - 1:
                firstChar = '+'
                otherChars = '-'
            else:
                firstChar = '|'
                otherChars = ' '
            s += firstChar + (otherChars * (self.indentSize - 1))
        return s
    def printPath (self, path, bytes, pct, isDir, depth):
        indentStr = self.getIndentStr(depth, isDir)
        if path:
            if self.units == 'k':
                print '%s%-11.1f %3.0f%% %s' % (indentStr, bytes / 1000.0, pct, path)
            elif self.units == 'm':
                print '%s%-7.1f %3.0f%% %s' % (indentStr, bytes / 1000000.0, pct, path)
            else:
                print '%s%-12ld %3.0f%% %s' % (indentStr, bytes, pct, path)
        else:
            print indentStr
    def isDir (self, item):
        # Directories have 3 entries (size, path, list of contents) while files
        # have 2 (size, path).
        return len(item) == 3
    def printDir (self, path, dsize, pct, items, depth):
        # Print entire tree starting with given directory
        self.printPath(path, dsize, pct, True, depth)
        count = 0
        cumBytes = 0
        dir = True
        for item in items:
            size = item[0]
            path = item[1]
            dir = self.isDir(item)
            if dsize > 0:
                pct = size * 100.0 / dsize
            else:
                pct = 0.0
            if dir:
                dirContents = item[2]
                self.printDir(path, size, pct, dirContents, depth+1)
            else:
                self.printPath(path, size, pct, False, depth+1)
            count += 1
            cumBytes += size

        # Add blank line if the last entry shown is a file
        ### if not dir:
        ###     printPath('', 0, 0, False, depth, options)
    def dirSize (self, dirPath, depth):
        # For given directory, returns the list [size, [entry-1, entry-2, ...]]
        total = 0L
        try:
            dirList = os.listdir (dirPath)
        except:
            if isdir (dirPath):
                print 'Cannot list directory %s' % dirPath
            return 0
        itemList = []
        for item in dirList:
            if item.startswith('.'):
                continue # it is hidden, mean hack i know but you can't be great everywhere, will be changed
            path = '%s/%s' % (dirPath, item)
            try:
                stats = os.stat (path)
            except:
                # print 'Cannot stat %s' % path
                # written to log later...
                continue
            size = stats[6]
            if isdir (path) and (self.followLinks or
                                 (not self.followLinks and not islink (path))):
                dsize, items = self.dirSize (path, depth + 1)
                size += dsize
                if self.maxDepth == -1 or depth < self.maxDepth:
                    itemList.append([size, item, items])
            elif self.showFiles:
                if self.maxDepth == -1 or depth < self.maxDepth:
                    itemList.append([size, item])
            total += size
            # Sort in descending order
        itemList.sort()
        itemList.reverse()

        # Keep only the items that will be displayed
        cumBytes = 0
        i = 0
        for i, v in enumerate(itemList):
            size = v[0]
            path = v[1]
            showItem = True
            if self.topNOption == 'p':
                showItem = (size * 100.0 / total) >= self.percent
            if showItem:
                if self.topNOption == 'n':
                    if self.topN and (i + 1) == self.topN:
                        break
                elif self.topNOption == 'c':
                    cumBytes += size
                    if (cumBytes * 100.0 / total) >= self.cumPercent:
                        break
            else:
                break
        if self.topNOption != 'p':
            # Need to keep the current item
            i += 1
        if i < len(itemList):
            itemList[i:] = []

        return [total, itemList]
    def execute(self):
        dsize, items = self.dirSize(self.directory, 0)
        self.printDir(self.directory, dsize, 100.0, items, 0)
    def end(self):
        print "end"