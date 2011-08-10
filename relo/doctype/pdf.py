#!/usr/bin/env python
# encoding: utf-8
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.interfaces import DocType

from pyPdf import PdfFileReader

import re

class PDF(DocType):
    name = "PDF Plugin"

    def load(self, path):
        self.path = path
        self.pdfObject = PdfFileReader(file(path, "rb"))

        self.content = ""
        for page in self.pdfObject.pages:
            self.content += page.extractText() + "\n"

    def search(self, key):
        if not (re.search(key, self.content) == None):
            for m in re.finditer(key, self.content):
                print "Found at position: " + str(m.start())
        else:
            print "Nothing found"

        print "Finished with: " + self.path