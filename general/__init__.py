import os
import doctype

__all__ = ['manage', 'interfaces']

def listFiles(rootDir, hidden):
    """
    list files in specified directory
    """
    fileList = []
    total_size = 0
    for root, subFolders, files in os.walk(rootDir):
        subFolders[:] = [sub for sub in subFolders if not sub.startswith('.')]
        for file in files:
            if file.startswith('.') and hidden==0:
                continue
            itempath = os.path.join(root, file)
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