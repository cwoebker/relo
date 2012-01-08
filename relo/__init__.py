#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import time
import math
import argparse
from relo import core
from relo.core.log import logger
from relo.core import config
from relo.core.config import conf
from relo.local.search import Search, IndexSearch, checkIndex
from relo.local.index import MetaIndex, InvertedIndex
from relo.local.stats import Stats
from relo.net import crawl as rawl
from relo.core.config import PATH_HOME_ETC
from relo.core.util import mkdirs

__author__ = "cwoebker"
__version__ = config.get_version()
__copyright__ = "© 2012 cwoebker"
__license__ = "See in LICENSE file"

def init_home():
    if not os.path.isdir(PATH_HOME_ETC):
        mkdirs(PATH_HOME_ETC)

def main():
    """
    parses the arguments and starts the application
    """
    parser = argparse.ArgumentParser(description='Recursive Document Content Search in Python')
    parser.add_argument('-v', '--version', action='version',
                        version=('%(prog)s ' + __version__))
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('-i', '--info', action='store_true', help='prints extra information')
    log_group.add_argument('-d', '--debug', action='store_true', help='prints debug information')
    reloParsers = parser.add_subparsers(help='sub-command help')

    ##### Config Arguments #####

    update = reloParsers.add_parser('update', help='update help')
    update.set_defaults(which='update')
    update.add_argument('key', help="master/develop")

    config = reloParsers.add_parser('config', help='config help')
    #config.set_defaults(which='config')
    configParsers = config.add_subparsers()
    list = configParsers.add_parser('list', help="lists all available config fields")
    list.set_defaults(which='config.list')
    read = configParsers.add_parser('read', help="read a specific option from the config")
    read.set_defaults(which='config.read')
    read.add_argument('key', help="config key")
    write = configParsers.add_parser('write', help="write a specific value to the config")
    write.set_defaults(which='config.write')
    write.add_argument('key', help="config key")
    write.add_argument('value', help="new value")

    ##### Local Argumnets #####

    ## INDEX

    index = reloParsers.add_parser('index', help='index help')
    index.set_defaults(which='index')

    index.add_argument('-s', '--hidden', '--secret', action='store_true',
        help='search hidden files')
    index.add_argument('directory', action='store', default='./',
        help='select directory')
    index_type_group = index.add_mutually_exclusive_group()
    index_type_group.add_argument('-m', '--meta', action='store_true',
        help='search match in fileNames')
    index_type_group.add_argument('-c', '--content', action='store_true',
        help='search match in content')

    ## STATS

    stats = reloParsers.add_parser('stats', help='analyze help')
    stats.set_defaults(which='stats')
    stats.add_argument('module', action='store', help='module to use')
    stats.add_argument('-s', '--hidden', '--secret', action='store_true',
                        help='take hidden files into account')
    stats.add_argument('-d', '--directory', action='store', default='./',
                        dest='directory', help='select directory')

    ## SEARCH

    search = reloParsers.add_parser('search', help='search help')
    search.set_defaults(which='search')
    search.add_argument('search_key', action='store', help='keyword to search for')

    search.add_argument('-s', '--hidden', '--secret', action='store_true',
                        help='search hidden files')
    search.add_argument('--filelog', action='store_true',
                        help='log is written to file - always in debug mode')
    search.add_argument('-r', '--recursive', action='store_true',
                        help='search recursively')
    search.add_argument('-f', '--forceSearch', action='store_true',
                        help='force a real file system search')
    doctype_group = search.add_mutually_exclusive_group()
    doctype_group.add_argument('-a', '--all', action='store_true',
                        help='search all files (even non supported with standard plugin)')
    doctype_group.add_argument('--doctype', action='store',
                        help='specify doctypes you want to use in your search')
    search_type_group = search.add_mutually_exclusive_group()
    search_type_group.add_argument('-n', '--name', action='store_true',
                            help='search match in fileNames (regex allowed) - (default)')
    search_type_group.add_argument('-c', '--content', action='store_true',
                            help='search match in content (regex allowed)')
    log_group = search.add_mutually_exclusive_group()
    log_group.add_argument('--info', action='store_true',
                            help='enable info mode')
    log_group.add_argument('--debug', '--verbose', action='store_true',
                        help='enable debug/verbose mode')

    search.add_argument('-d', '--directory', action='store', default='./',
                        dest='directory', help='select Directory - (default=current)')

    ##### Remote Argumnets #####

    crawl = reloParsers.add_parser('crawl', help='crawl help')
    crawl.set_defaults(which='crawl')
    crawl.add_argument('url', action='store', help='url to use')

    try:
        results = parser.parse_args(args=sys.argv[1:])
        ########## PREP ##########
        if results.info:
            logger.level = 1
        elif results.debug:
            logger.level = 2

    except IOError, msg:
        parser.error(str(msg))
        logger.error(str(msg))
        return 1

    ########## INIT ##########
    logger.debug(results)
    core.init()


    ########## CONFIG ##########
    if results.which.startswith('config'):
        if results.which == 'config.list':
            conf.listConfig(None)
        if results.which == 'config.write':
            conf.writeConfig(results.key, results.value)
        if results.which == 'config.read':
            print conf.readConfig(results.key)
    ########## UPDATE ##########
    elif results.which == 'update':
        from relo.core.update import ReloUpdater
        curVersion = __version__
        relo = ReloUpdater(curVersion)
        if results.key in ['master', 'develop']:
            relo.update(results.key)
        else:
            logger.error('Invalid Repo-Key')
    ########## CRAWL ##########
    elif results.which == 'crawl':
        url = results.url

        sTime = time.time()

        crawler = rawl.Crawler(url, 16)
        crawler.crawl()
        print "\n".join(crawler.urls)

        eTime = time.time()
        tTime = eTime - sTime

        print "Found:    %d" % crawler.links
        print "Followed: %d" % crawler.followed
        print "Stats:    (%d/s after %0.2fs)" % (int(math.ceil(float(crawler.links) / tTime)), tTime)
    ########## SEARCH ##########
    elif results.which == 'search':
        check = checkIndex(results.directory)
        if check is not None and not results.forceSearch:
            logger.info("Index found.")
            search = IndexSearch(results.directory, results.search_key)
            if results.content:
                search.contentSearch()
            else:
                search.nameSearch()
            search.printResult()
        else:
            search = Search(results.info, results.debug, results.all, results.hidden, results.filelog, results.content, results.recursive,
                    results.doctype, results.directory, results.search_key)
            search.list()
            search.filter()
            search.start()
    ########## INDEX ##########
    elif results.which == 'index':
        if results.meta:
            meta = MetaIndex(results.directory, results.hidden)
            meta.setUpProject('meta')
            meta.listProject()
            meta.run()
        elif results.content:
            inverted = InvertedIndex(results.directory, results.hidden)
            inverted.setUpProject('search')
            inverted.listProject()
            inverted.run()
        else:
            line = "Relo: Meta + Search Index"
            logger.head(line)
            logger.log('-' * len(line))
            sTime = time.time()
            meta = MetaIndex(results.directory, results.hidden)
            meta.listProject()
            meta.run()
            inverted = InvertedIndex(results.directory, results.hidden)
            inverted.setUpProject('meta:::search') ### make index more modular and fix this nasty code
            inverted.run()
            eTime = time.time()
            dTime = eTime - sTime
            logger.info("(Meta+Search: %0.2fs)" % (dTime))
    ########## STATS ##########
    elif results.which == 'stats':
        stats = Stats(results.directory, results.module, results.hidden)
        if stats.check():
            stats.go()
        else:
            stats.list()