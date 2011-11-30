#!/usr/bin/env python
#encoding: utf-8

#####################################################################
########################## Global Variables #########################
#####################################################################
## Define any global variables here that do not need to be changed ##
#####################################################################
#####################################################################

VERSION = (0, 6, 0, 'beta')

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3]:
        version = '%s %s' % (version, VERSION[3])
    return version

EXAMPLE_VARIABLE = "testString"