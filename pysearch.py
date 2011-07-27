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

__author__ = "cwoebker"
__version__ = "$Revision: 0.0.1 $"
__date__ = "$Date: 2011/07/26"
__copyright__ = "cwoebker"
__license__ = "GPL"

directory = "./"
_verbose = 0
_hidden = 0
_type = ""

import sys, getopt
#import log
import docs
import general.listing

class pySearch:
    def __init__(self):
        """
        Main pySearch class
        """
        print "pySearch class initialized"
        print "Verbose: " + str(bool(_verbose))
        #self.searchLog = log.searchLogger(_verbose)
        #print "pySearch Logger initialized"

    def list(self, dir):
        #self.searchLog.info("Listing directory content...")
        #self.searchLog.info("Supported File Types: " + repr(docs.supported))
        print "Listing directory content..."
        print "Supported File Types: " + repr(docs.supported)
        general.listing.listFiles(dir, _hidden)
        
    def validate(self):
        sure = raw_input("Are you sure you want to perform the given search? (y/n) ")
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
        opts, args = getopt.getopt(argv, "hd:v", ["help", "directory", "hidden"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-v':
            global _verbose
            _verbose = 1
        elif opt == "--hidden":
            global _hidden
            _hidden = 1
        elif opt in ("-d", "--directory"):
            global directory
            directory = str(arg)

    search = pySearch()
    search.validate()
    search.list(directory)

if __name__ == '__main__':
    main(sys.argv[1:])