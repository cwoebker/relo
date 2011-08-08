#!/usr/bin/env python
# encoding: utf-8
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from general.interfaces import DocType

import re

class PDF(DocType):
    name = "PDF Plugin"

    def load(self, path):
        self.path = path
        self.pdfObject = PdfFileReader(file(path, "rb"))

        pageText = []
        for page in self.pdfObject.pages:
            print 'page'
            pageText.append(page.extractText())

        print pageText
        test = input()

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