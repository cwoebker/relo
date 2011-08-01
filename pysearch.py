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

_directory = "./"
_verbose = 0
_hidden = 0
_type = ""

import sys, getopt
import argparse
import doctype
import general.manage

class pySearch:
    def __init__(self):
        """
        Main pySearch class
        """
        self.verbose = _verbose
        self.hidden = _hidden
        self.type = _type
        self.dir = _directory
        
        print "pySearch: version %s" % __version__
        print "Verbose: " + str(bool(self.verbose))
        print "Hidden Files: " + str(bool(self.hidden))
        print "Search Type: " + self.type
        print "Directory: " + self.dir

        self.filteredList = []
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

    def start(self, key):
        manager = general.manage.Manager(key)
        for item in self.filteredList:
            manager.start(item)

    def startName(self, key):
        general.fileNameSearch(self.fileList, key)

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
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))

    '''try:
        opts, args = getopt.getopt(argv, "hd:t:av", ["help", "directory", "type", "all"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    print "Arguments: " + repr(args)
    print "Options: " + repr(opts)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif opt in ("-d", "--directory"):
            global _directory
            _directory = arg
        elif opt in ("-t", "--type"):
            global _type
            _type = arg
        elif opt in ("-a", "--all"):
            global _hidden
            _hidden = 1
        elif opt == '-v':
            global _verbose
            _verbose = 1'''


    search = pySearch()
    search.validate()
    search.list()
    if _type == "name":
        search.startName(args[0])
    elif _type == "regex":
        search.filter()
        pass
    else:
        search.filter()
        search.start(args[0])

if __name__ == '__main__':
    main(sys.argv[1:])