#!/usr/bin/env python
# encoding: utf-8
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.interfaces import DocType

from pyPdf import PdfFileReader

class PDF(DocType):
    name = "PDF Plugin"

    def load(self, path):
        self.path = path
        self.pdfObject = PdfFileReader(file(path, "rb"))

        self.content = ""
        for page in self.pdfObject.pages:
            self.content += page.extractText() + "\n"