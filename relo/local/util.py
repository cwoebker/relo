#!/usr/bin/env python
# encoding: utf-8

import os
from collections import defaultdict
from relo.core import doctype
from relo.core.log import logger

FILE_Marker = '<files>'

##### Format #####

def paths2tree(paths):
    "a list of paths to a list of tree elements"
    def attach(branch, trunk):
        """
        Insert a branch of directories on its trunk
        """
        parts = branch.split('/', 1)
        if len(parts) == 1: # is a file
            trunk[FILE_Marker].append(parts[0])
        else: # is a directory
            node, others = parts
            if node not in trunk:
                trunk[node] = defaultdict(dict, ((FILE_Marker, []),))
            attach(others, trunk[node])


    main_dict = defaultdict(dict, ((FILE_Marker, []),))
    for path in paths:
        attach(path, main_dict)
    return main_dict

def tree2paths(tree):
    "a list of tree elements to a list of paths"
    for key, value in tree.iteritems():
        #print key + ' -+- ' + repr(value)
        #NOT WORKING YEY
        #CAN BE DERIVED FROM PRINT TREE FUNCTION
        pass

def printTree(tree, indent=0):
    """
    Print the file tree structure with proper indentation.
    """
    for key, value in tree.iteritems():
        if key == FILE_Marker:
            if value:
                print '  ' * indent + str(value)
        else:
            print ' ' * indent + str(key)
            if isinstance(value, dict):
                printTree(value, indent+1)
            else:
                print '  ' * (indent+1) + str(value)


##### Listing #####

def countFiles(rootDir):
    count = 0
    for path, dirs, files in os.walk(rootDir):
        for file in files:
            if file.startswith('.'):
                continue
            itempath = os.path.join(path, file)
            if os.path.islink(itempath):
                continue
            count += 1
    return count

def getTotalSize(rootDir, hidden):
    """
    get total size in directory (recursively)
    """
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
    return total_size

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

##### List Conversion #####

def paths2names(pathList):
    """
    takes a list of path
    returns list of names
    """
    nameList = []
    for item in pathList:
        name = os.path.basename(item)
        nameList.append(name)
    return nameList