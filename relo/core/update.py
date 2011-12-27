#!/usr/bin/env python
# encoding: utf-8

from relo.core.log import logger
from relo.core.config import conf, RELO_DEVELOP_VERSION_URL, RELO_MASTER_VERSION_URL
import urllib

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
    def check(self):
        if self.key == 'master':
            url = RELO_MASTER_VERSION_URL
        elif self.key == 'develop':
            url = RELO_DEVELOP_VERSION_URL
        logger.log('Checking remote version...')
        remote = urllib.urlopen(url)
        self.remoteVersion = remote.read()
    def update(self, key):
        self.key = key
        self.check()

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