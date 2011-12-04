#!/usr/bin/env python
# encoding: utf-8

import os
from relo.core import doctype
import logging
logger = logging.getLogger('relo.log')

##### Listing #####

def listFiles(rootDir, hidden):
    returnList = []
    total_size = 0
    fileList = os.listdir(rootDir)
    for file in fileList:
        if file.startswith('.') and hidden==0:
            continue
        itempath = os.path.join(rootDir, file)
        if os.path.isdir(itempath) or os.path.islink(itempath):

            continue
        total_size += os.path.getsize(itempath)
        returnList.append(itempath)

    logger.debug("Total Size: %d" % total_size)
    return total_size, returnList

def recursiveListFiles(rootDir, hidden):
    """
    list files in specified directory
    """
    fileList = []
    total_size = 0
    for root, subFolders, files in os.walk(rootDir):
        if not hidden:
            subFolders[:] = [sub for sub in subFolders if not sub.startswith('.')]
        #print root
        for file in files:
            if file.startswith('.') and hidden==0:
                continue
            itempath = os.path.join(root, file)
            if os.path.islink(itempath):
                #print "link found" + itempath
                continue
            total_size += os.path.getsize(itempath)
            fileList.append(itempath)

    logger.debug("Total Size: %d" % total_size)
    return total_size, fileList

##### Filters #####

def filterList(fileList):
    filteredList = []
    for path in fileList:
        ext = getFileType(path)
        if ext in doctype.__all__:
            filteredList.append(path)
    return filteredList

def filterDocType(fileList, doctype):
    filteredList = []
    for path in fileList:
        ext = getFileType(path)
        if ext == doctype:
            filteredList.append(path)
    return filteredList

##### Information #####

def getFileType(itempath):
    """
    takes a path and returns a filetype
    """
    ext = os.path.splitext(itempath)[1]
    ext = ext.lstrip('.')
    return ext