#!/usr/bin/env python
#encoding: utf-8

#####################################################################
########################## Global Variables #########################
#####################################################################
## Define any global variables here that do not need to be changed ##
#####################################################################
#####################################################################
import os
import ConfigParser

VERSION = (0, 6, 0, 'beta')

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3]:
        version = '%s %s' % (version, VERSION[3])
    return version

class ReloConfig(object):
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
    def createDefaultConfig(self):
        ### config section for the core module
        self.config.add_section('core')

        self.config.set('core', 'version', VERSION)

        ### config section for the local module
        self.config.add_section('local')

        ### config section for the net module
        self.config.add_section('net')

        ### Creating configfile
        home = os.getenv('HOME')
        print "Need to create config file."
        os.system("touch ~/.relo")
        with open(os.path.join(home,'.relo'), 'wb') as configfile:
            print "Config File created"
            self.config.write(configfile)

    def checkConfig(self):
        home = os.getenv('HOME')
        if os.path.isfile(os.path.join(home, '.relo')):
            return True
        try:
            open(os.path.join(home, '.relo'))
        except IOError as e:
            print 'Config does not exist'
            return False

    def loadConfig(self):
        home = os.getenv('HOME')
        self.config.read(os.path.join(home, '.relo'))
    def saveConfig(self):
        pass
    def listConfig(self, category):
        if category == None:
            print self.config
    def readConfig(self, key):
        section, option = key.split('.')
        print self.config.get(section, option)
    def writeConfig(self, key, value):
        section, option = key.split('.')
        self.config.set(section, option, value)
conf = ReloConfig()