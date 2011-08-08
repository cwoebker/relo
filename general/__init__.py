import os
import doctype

__all__ = ['manage', 'interfaces']


VERSION = (0, 3, 0, 'alpha')

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3]:
        version = '%s %s' % (version, VERSION[3])
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version

def listFiles(rootDir, hidden):
    returnList = []
    total_size = 0
    fileList = os.listdir(rootDir)
    for fname in fileList:
        itempath = os.path.join(rootDir, fname)
        if os.path.isdir(itempath) or os.path.islink(itempath):

            continue
        total_size += os.path.getsize(itempath)
        returnList.append(itempath)

    print "Total Size:", str(total_size)
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
        for file in files:
            if file.startswith('.') and hidden==0:
                continue
            itempath = os.path.join(root, file)
            if os.path.islink(itempath):
                continue
            total_size += os.path.getsize(itempath)
            fileList.append(itempath)

    print "Total Size:", str(total_size)
    return total_size, fileList

def getFileType(itempath):
    """
    takes a path and returns a filetype
    """
    ext = os.path.splitext(itempath)[1]
    ext = ext.lstrip('.')
    return ext

def filterList(fileList):
    filteredList = []
    for path in fileList:
        ext = getFileType(path)
        if ext in doctype.supported:
            filteredList.append(path)

    return filteredList

def fileNameSearch(fileList, key):
    for itempath in fileList:
        item = os.path.basename(itempath)
        if not item.find(key) == -1:
            print "Found: " + itempath