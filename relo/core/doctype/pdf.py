#!/usr/bin/env python
# encoding: utf-8
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.interfaces import DocType

#from pyPdf import PdfFileReader
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from cStringIO import StringIO

class PDF(DocType):
    name = "PDF Plugin"

    def load(self, path):
        #self.path = path
        #self.pdfObject = PdfFileReader(file(path, "rb"))

        #self.content = ""
        #for page in self.pdfObject.pages:
        #    self.content += page.extractText() + "\n"
        self.path = path
        rsrcmgr = PDFResourceManager()
        restr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, restr, codec=codec, laparams=laparams)

        fp = file(path, 'rb')
        process_pdf(rsrcmgr, device, fp)
        fp.close()
        device.close()

        self.content = restr.getvalue()
        restr.close()
        return self.content
