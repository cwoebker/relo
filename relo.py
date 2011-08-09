#!/usr/bin/env python

import general

__author__ = "cwoebker"
__version__ = general.get_version()
__copyright__ = "cwoebker"
__license__ = "See in LICENSE file"

import sys
import argparse
import doctype
import general.manage
import yapsy

class Relo:
    def __init__(self, _debug, _hidden, _type, _recursive, _directory, _key):
        """
        Main Relo class
        """
        self.verbose = _debug
        self.hidden = _hidden
        self.recursive = _recursive
        self.dir = _directory
        self.key = _key
        
        print "Relo: version %s" % __version__
        print "Verbose: " + str(bool(self.verbose))
        print "Hidden Files: " + str(bool(self.hidden))
        print "Recursive: " + str(bool(self.recursive))
        print "Search Type: " + _type
        print "Directory: " + self.dir
        print "Searching for: " + self.key

        self.filteredList = []
        self.extList = []
        self.total_size = 0
        self.fileList = []

    def list(self):
        if self.recursive:
            print "Listing directory content recursively..."
            self.total_size, self.fileList = general.recursiveListFiles(self.dir, self.hidden)
        else:
            print "Listing directory content..."
            self.total_size, self.fileList = general.listFiles(self.dir, self.hidden)
        print "Supported File Types: " + repr(doctype.__all__)

    def filter(self):
        self.filteredList = general.filterList(self.fileList)
        for itempath in self.filteredList:
            item = general.getFileType(itempath)
            if item not in self.extList:
                self.extList.append(item)

    def start(self):
        manager = general.manage.Manager(self.key, self.extList)
        for item in self.filteredList:
            manager.start(item)

    def startName(self):
        general.fileNameSearch(self.fileList, self.key)

def main(argv):
    """
    parses the arguments and starts the application
    """
    parser = argparse.ArgumentParser(description='Recursive Document Content Search in Python')
    parser.add_argument('search_key', action='store', help='keyword to search for')
    parser.add_argument('-v', '--version', action='version',
                        version=('%(prog)s ' + __version__))
    parser.add_argument('-d', '--directory', action='store', default='./',
                        dest='directory', help='select Directory - (default=current)')
    parser.add_argument('-a', '--all', action='store_true',
                        help='search all files/hidden files')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='search recursively')
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument('-n', '--name', action='store_true',
                            help='search match in fileNames (regex allowed) - (default)')
    type_group.add_argument('-c', '--content', action='store_true',
                            help='search match in content (regex allowed)')
    parser.add_argument('--debug', '--verbose', action='store_true',
                        help='enable debug/verbose mode')
    
    try:
        results = parser.parse_args(args=argv)
    except IOError, msg:
        parser.error(str(msg))
    print results

    if results.name:
        type = "fileName Search"
    elif results.content:
        type = "content Search"
    else:
        type = "fileName Search"
    search = Relo(results.debug, results.all, type, results.recursive,
                      results.directory, results.search_key)
    search.list()
    if results.content:
        search.filter()
        search.start()
    else:
        search.startName()

if __name__ == '__main__':
    main(sys.argv[1:])