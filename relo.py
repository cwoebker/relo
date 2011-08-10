#!/usr/bin/env python

import sys
import argparse
import relo
from relo import Relo
from relo import yapsy

__author__ = "cwoebker"
__version__ = relo.get_version()
__copyright__ = "cwoebker"
__license__ = "See in LICENSE file"

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