#!/usr/bin/env python
#encoding: utf-8

#####################################################################
########################## Global Variables #########################
#####################################################################
## Define any global variables here that do not need to be changed ##
#####################################################################
#####################################################################
import os
import re
try:
    import ConfigParser
except:
    import configparser as ConfigParser

# relo version
VERSION = (0, 6, 'beta')

def get_version():
    return '%s.%s' % (VERSION[0], VERSION[1])
def get_long_version():
    return '%s.%s %s' % (VERSION[0], VERSION[1], VERSION[2])

# relo installer root path
INSTALLER_ROOT = os.path.dirname(os.path.abspath(__file__))

###### Root #####
# relo root path
ROOT = os.environ.get("RELO_ROOT")
if not ROOT:
    ROOT = os.path.join(os.environ["HOME"], ".relo")

# directories
PATH_ETC = os.path.join(ROOT, 'etc')
PATH_BIN = os.path.join(ROOT, 'bin')
PATH_LOG = os.path.join(ROOT, 'log')

PATH_SCRIPTS = os.path.join(ROOT, 'scripts')

# files
PATH_BIN_RELO = os.path.join(PATH_BIN, 'relo')
PATH_ETC_CONFIG = os.path.join(PATH_ETC, 'config.cfg')

##### Home #####
# relo home path
PATH_HOME = os.environ.get("RELO_HOME")
if not PATH_HOME:
    PATH_HOME = os.path.join(os.environ["HOME"], ".relo")

# directories
PATH_HOME_ETC = os.path.join(PATH_HOME, 'etc')

# files

##### Config #####
class ReloConfig(object):
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
    def loadConfig(self):
        self.config.read([PATH_ETC_CONFIG, os.path.join(INSTALLER_ROOT, 'etc', 'config.cfg')])
    def saveConfig(self):
        self.config.write(PATH_ETC_CONFIG)
    def listConfig(self, category):
        def listCore():
            print "[Core]"
            for item in self.config.items('core'):
                print " - " + str(item)
        def listLocal():
            print "[Local]"
            for item in self.config.items('local'):
                print " - " + str(item)
        def listNet():
            print "[Net]"
            for item in self.config.items('net'):
                print " - " + str(item)
        if category == None or category == 'core':
            listCore()
        if category == None or category == 'local':
            listLocal()
        if category == None or category == 'net':
            listNet()
        else:
            print "category not found"


    def readConfig(self, key):
        section, option = key.split('.')
        return self.config.get(section, option)
    def writeConfig(self, key, value):
        section, option = key.split('.')
        self.config.set(section, option, value)
conf = ReloConfig()
conf.loadConfig()

### Relo Downloads ###
RELO_UPDATE_URL_MASTER = conf.readConfig('core.master')
RELO_UPDATE_URL_DEVELOP = conf.readConfig('core.develop')
RELO_UPDATE_URL_PYPI = conf.readConfig('core.pypi')
RELO_UPDATE_URL_CONFIG = conf.readConfig('core.config')

RELO_MASTER_VERSION_URL = conf.readConfig('core.master-version')
RELO_DEVELOP_VERSION_URL = conf.readConfig('core.develop-version')

### Relo Index -> move to config file later
##### Inverted Index Variables #####

# Words which should not be indexed
STOP_WORDS = ("the", "of", "to", "and", "a", "in", "is", "it", "you", "that")

# Do not index any words shorter than this
MIN_WORD_LENGTH = 3

# Consider these characters to be punctuation (they will be replaced with spaces prior to word extraction)
PUNCTUATION_CHARS = ".,;:!?@£$%^&*()-–<>[]{}\\|/`~'\""

# A redis key to store a list of metaphones present in this project
REDIS_KEY_METAPHONES = "id:%(project_id)s:metaphones"

# A redis key to store a list of item IDs which have the given metaphone within the given project
REDIS_KEY_METAPHONE = "id:%(project_id)s:mp:%(metaphone)s"

# A redis key to store a list of documents present in this project
REDIS_KEY_DOCUMENTS = "id:%(project_id)s:docs"

# A redis key to store meta information which are associated with the document within the given project
REDIS_KEY_DOCUMENT = "id%(project_id)s:doc:%(document)s"

# A redis key to store a list of projects stored in the database
REDIS_KEY_PROJECTS = "projects"