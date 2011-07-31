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

directory = "./"
_verbose = 0
_hidden = 0
_type = ""

import sys, getopt
#import log
import doctype
import general.manage

class pySearch:
    def __init__(self):
        """
        Main pySearch class
        """
        self.verbose = _verbose
        self.hidden = _hidden
        
        print "pySearch: version %s" % __version__
        print "Verbose: " + str(bool(self.verbose))
        print "Hidden Files: " + str(bool(self.hidden))

        self.filteredList = []
        self.total_size = 0
        self.fileList = []

    def list(self, dir):
        #self.searchLog.info("Listing directory content...")
        #self.searchLog.info("Supported File Types: " + repr(doctype.supported))
        print "Listing directory content..."
        print "Supported File Types: " + repr(doctype.__all__)
        self.total_size, self.fileList = general.listFiles(dir, _hidden)

    def filter(self):
        self.filteredList = general.filterList(self.fileList)

    def start(self, key):
        manager = general.manage.Manager(key)
        for item in self.filteredList:
            manager.start(item)

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
    try:
        opts, args = getopt.getopt(argv, "hd:v", ["hidden", "directory", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--hidden"):
            global _hidden
            _hidden = 1
        elif opt == '-v':
            global _verbose
            _verbose = 1
        elif opt == "--help":
            usage()
            sys.exit(1)
        elif opt in ("-d", "--directory"):
            global directory
            directory = str(arg)

    search = pySearch()
    search.validate()
    search.list(directory)
    search.filter()
    search.start(args[0])

if __name__ == '__main__':
    main(sys.argv[1:])