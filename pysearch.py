#!/usr/bin/env python
"""
------------------------------------------------------------
Recursive Document Search - Python (pySearch)

Searches content of documents in a specific directory

Usage: python pysearch.py [options] [arguments]

Options:
  -h,  --help           shows this help

  -d                    show debugging information while running
  -v                    show verbose output while running

Examples:
  apm.py

This program is developed and maintained by Cecil Woebker.
------------------------------------------------------------
"""
import general

__author__ = "cwoebker"
__version__ = general.get_version()
__copyright__ = "cwoebker"
__license__ = "See in LICENSE file"

import sys
import argparse
import doctype
import general.manage

class pySearch:
    def __init__(self, _debug, _hidden, _type, _directory, _key):
        """
        Main pySearch class
        """
        self.verbose = _debug
        self.hidden = _hidden
        self.dir = _directory
        self.key = _key
        
        print "pySearch: version %s" % __version__
        print "Verbose: " + str(bool(self.verbose))
        print "Hidden Files: " + str(bool(self.hidden))
        print "Search Type: " + _type
        print "Directory: " + self.dir
        print "Searching for: " + self.key

        self.filteredList = []
        self.extList = []
        self.total_size = 0
        self.fileList = []

    def list(self):
        #self.searchLog.info("Listing directory content...")
        #self.searchLog.info("Supported File Types: " + repr(doctype.supported))
        print "Listing directory content..."
        print "Supported File Types: " + repr(doctype.__all__)
        self.total_size, self.fileList = general.listFiles(self.dir, self.hidden)

    def filter(self):
        self.filteredList = general.filterList(self.fileList)
        for item in self.filteredList:
            if item not in self.extList:
                self.extList.append(item)

    def start(self):
        manager = general.manage.Manager(self.key, self.extList)
        for item in self.filteredList:
            manager.start(item)

    def startName(self):
        general.fileNameSearch(self.fileList, self.key)

    def validate(self):
        sure = 'y' #raw_input("Are you sure you want to perform the given search? (y/n) ")
        if sure != 'y':
            sys.exit(2)

def usage():
    """
    prints usage information
    """
    print __doc__

def main(argv):
    """
    parses the arguments and starts the application
    """
    parser = argparse.ArgumentParser(description='Recursive Document Content Search in Python')
    parser.add_argument('search_key', action='store', help='keyword to search for')
    parser.add_argument('-v', '--version', action='version',
                        version=('%(prog)s ' + __version__))
    parser.add_argument('-d', '--directory', action='store', default='./',
                        dest='directory', help='select Directory to search in')
    parser.add_argument('-a', '--all', action='store_true',
                        help='show all files/hidden files')
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument('-n', '--name', action='store_true',
                            help='search match in fileNames')
    type_group.add_argument('-c', '--content', action='store_true',
                            help='search match in content')
    parser.add_argument('--debug', '--verbose', action='store_true',
                        help='enable debug/verbose debugging')
    
    '''doctype_group = parser.add_argument_group('doctype arguments')
    doctype_group.add_argument('--txt', action='store_true', default=False)
    doctype_group.add_argument('--log', action='store_true', default=False)'''
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
    search = pySearch(results.debug, results.all, type,
                      results.directory, results.search_key)
    search.validate()
    search.list()
    if results.name:
        search.startName()
    elif results.content:
        search.filter()
        search.start()

if __name__ == '__main__':
    main(sys.argv[1:])