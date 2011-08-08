#!/usr/bin/env python
# encoding: utf-8
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from general.interfaces import DocType

import re

class TXT(DocType):
    name = "TXT Plugin"
    sname = "txt"
    
    def load(self, path):
        self.path = path
        self.fobj = open(path, "r")
        self.content = ""
        for line in self.fobj:
            self.content += line
        self.fobj.close()

    def search(self, key):
        if not (re.search(key, self.content) == None):
            for m in re.finditer(key, self.content):
                print "Found at position: " + str(m.start())
        else:
            print "Nothing found"
            
        print "Finished with: " + self.path