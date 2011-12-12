import string, sys, os, getopt
from os.path import *

boolStrings = ['off', 'on']

class Options:
    """Holds program options as object attributes"""
    def __init__(self):
        # When adding a new option, initialize it here.
        self.cumPercent = 80
        self.topNOption = 'n'
        self.maxDepth = 2
        self.showFiles = False
        self.indentSize = 4
        self.followLinks = False
        self.topN = 5
        self.percent = 10
        self.units = 'k'

    def dump(self):
        print 'Options:'
        print 'TopN option = %s' % self.topNOption
        if self.topNOption == 'c':
            print 'Cumulative percentage = %d' % self.cumPercent
        elif self.topNOption == 'p':
            print 'Percentage = %d' % self.percent
        else:
            if self.topN > 0:
                print 'TopN = %d' % self.topN
            else:
                print 'TopN = all'
        if self.maxDepth >= 0:
            print 'Max depth = %d' % self.maxDepth
        else:
            print 'Max depth = any'
        print 'Show files = %s' % (boolStrings[self.showFiles])
        print 'Indent size = %d' % self.indentSize
        print 'Follow links = %s' % (boolStrings[self.followLinks])
        print 'Units = %s' % self.units
        print

def getIndentStr(depth, isDir, options):
    s = ''
    for i in range(depth):
        if isDir and i == depth - 1:
            firstChar = '+'
            otherChars = '-'
        else:
            firstChar = '|'
            otherChars = ' '
        s += firstChar + (otherChars * (options.indentSize - 1))
    return s

def printPath (path, bytes, pct, isDir, depth, options):
    indentStr = getIndentStr(depth, isDir, options)
    if path:
        if options.units == 'k':
            print '%s%-11.1f %3.0f%% %s' % (indentStr, bytes / 1000.0, pct, path)
        elif options.units == 'm':
            print '%s%-7.1f %3.0f%% %s' % (indentStr, bytes / 1000000.0, pct, path)
        else:
            print '%s%-12ld %3.0f%% %s' % (indentStr, bytes, pct, path)
    else:
        print indentStr

def isDir (item):
    # Directories have 3 entries (size, path, list of contents) while files
    # have 2 (size, path).
    return len(item) == 3

def printDir (path, dsize, pct, items, depth, options):
    # Print entire tree starting with given directory
    printPath(path, dsize, pct, True, depth, options)
    count = 0
    cumBytes = 0
    dir = True
    for item in items:
        size = item[0]
        path = item[1]
        dir = isDir(item)
        if dsize > 0:
            pct = size * 100.0 / dsize
        else:
            pct = 0.0
        if dir:
            dirContents = item[2]
            printDir(path, size, pct, dirContents, depth+1, options)
        else:
            printPath(path, size, pct, False, depth+1, options)
        count += 1
        cumBytes += size

    # Add blank line if the last entry shown is a file
    ### if not dir:
    ###     printPath('', 0, 0, False, depth, options)

def dirSize (dirPath, depth, options):
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
        path = '%s/%s' % (dirPath, item)
        try:
            stats = os.stat (path)
        except:
            print 'Cannot stat %s' % path
            continue
        size = stats[6]
        if isdir (path) and (options.followLinks or
                             (not options.followLinks and not islink (path))):
            dsize, items = dirSize (path, depth + 1, options)
            size += dsize
            if options.maxDepth == -1 or depth < options.maxDepth:
                itemList.append([size, item, items])
        elif options.showFiles:
            if options.maxDepth == -1 or depth < options.maxDepth:
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
        if options.topNOption == 'p':
            showItem = (size * 100.0 / total) >= options.percent
        if showItem:
            if options.topNOption == 'n':
                if options.topN and (i + 1) == options.topN:
                    break
            elif options.topNOption == 'c':
                cumBytes += size
                if (cumBytes * 100.0 / total) >= options.cumPercent:
                    break
        else:
            break
    if options.topNOption != 'p':
        # Need to keep the current item
        i += 1
    if i < len(itemList):
        itemList[i:] = []

    return [total, itemList]

def usage (name):
    options = Options()
    print '''
usage: %s [-c percent|-n top-n|-p percent] [-d depth] [-f on|off] [-i indent-size] [-l on|off] [-u b|k|m] dir [dir...]'
    -c    Cumulative percent contribution (default = %d)
    -d    Max depth of directories. '-d any' => no limit. (default = %d)
    -f    Show files (default = %s)
    -i    Indent size (default = %d)
    -l    Follow symbolic links (Unix only. default = %s)
    -n    The N in top-N. '-n all' => show all. (default = %d)
    -p    Percent contribution of each directory/file (defalut = %d)
    -u    Units to display size (default = %s)
            b    Bytes
            k    Kilobytes. k = 1000
            m    Megabytes. m = 1,000,000

Only one of -c, -n and -p can be specified. This controls how
many entries are shown for each directory. The default is -%s.
With -n, only the top N entries are shown.
With -c, the top entries that together contribute the given
percentage of a directory's size are shown.
With -p, all entries that contribute the given percentage or
greater of a directory's size are shown.

''' % (name, options.cumPercent, options.maxDepth,
        boolStrings[options.showFiles], options.indentSize,
        boolStrings[options.followLinks], options.topN,
        options.percent, options.units, options.topNOption)