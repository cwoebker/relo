#!/usr/bin/env python
# encoding: utf-8

from relo.core.log import logger
from relo.core.config import conf, RELO_DEVELOP_VERSION_URL, RELO_MASTER_VERSION_URL, RELO_UPDATE_URL_DEVELOP, RELO_UPDATE_URL_MASTER
from relo.core.exceptions import UpdateException
import tarfile
import urllib
import sys
import os
from relo.core import util
from relo.net.download import curl

class AbstractUpdater(object):
    def __init__(self):
        self.localVersion = 0
        self.remoteVersion = 0
    def getLocalVersion(self):
        pass
    def getRemoteVersion(self):
        pass
    def executeUpdate(self):
        pass

class ReloUpdater(AbstractUpdater):
    """
    Updates the relo library itself.
    """
    def __init__(self, curVersion):
        self.localVersion = curVersion
        try:
            float(self.localVersion)
        except:
            logger.error('Could not determine local version.')
            sys.exit()
    def check(self):
        if self.key == 'master':
            url = RELO_MASTER_VERSION_URL
        elif self.key == 'develop':
            url = RELO_DEVELOP_VERSION_URL
        remote = urllib.urlopen(url)
        self.remoteVersion = remote.read()
        try:
            float(self.remoteVersion)
        except:
            logger.error('Could not determine remote version.')
            sys.exit()
        logger.info('Local Version - ' + self.localVersion)
        logger.info('Remote Version - ' + self.remoteVersion)
        if float(self.remoteVersion) > float(self.localVersion):
            logger.log("Found new version: " + self.remoteVersion)
            return True
        else:
            logger.head("Already Up-To-Date")
            return False
    def download(self):
        if self.key == 'master':
            url = RELO_UPDATE_URL_MASTER
        elif self.key == 'develop':
            url = RELO_UPDATE_URL_DEVELOP
        logger.info('Download URL - %s' % url)
        self.localPath = os.path.join(os.getcwd(), 'tmp', 'relo-%s.tar.gz' % self.remoteVersion)
        try:
            curl(url, self.localPath)
        except:
            logger.error('Download error.')
            sys.exit()
    def extract(self):
        file = tarfile.open(self.localPath, 'r:gz')
        logger.debug('Archive opened')
        try:
            file.extractall(os.path.join(os.getcwd(), 'tmp'))
            file.close()
        except:
            logger.error('Extract error.')
            sys.exit()
    def update(self, key):
        self.key = key
        logger.head('Checking for update...')
        if self.check():
            util.mkdirs(os.path.join(os.getcwd(), 'tmp'))
            logger.head('Downloading relo... (%s)' % self.key)
            self.download()
            logger.head('Extracting update...')
            self.extract()
        else:
            sys.exit()

class DocTypeUpdater(AbstractUpdater):
    """
    Updates the doctype plugins that are used for local search.
    Own git repo for doctypes?!?
    """
    def __init__(self):
        super.__init__()
        localDocTypeList = []
        remoteDocTypeList = []
    def getLocalList(self):
        """
        Returns the local doctype plugins in list format.
        With the version number included
        [['pdf', 1.2],['txt', 2.1]]
        """
        pass
    def getRemoteList(self):
        pass
    def getLocalVersion(self):
        pass
    def getRemoteVersion(self):
        pass

class ExtensionUpdater(AbstractUpdater):
    """
    Updates relo's extensions.
    """
    def __init__(self):
        super.__init__()

class BackendUpdater(AbstractUpdater):
    """
    Updates index backends
    """
    def __init__(self):
        super.__init__()