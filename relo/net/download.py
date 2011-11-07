#!/usr/bin/env python
#encoding: utf-8

import sys, os
from os.path import basename
import urllib2
import urlparse
import shutil

class AbstractDownloader(object):
    def __init__(self):
        pass
    def url2name(self):
        return basename(urlsplit(url)[2])
    def download(url, localFileName = None):
        pass

class HTTPDownloader(AbstractDownloader):
    def __init__(self):
        pass
    def download(self, url, fileName = None):
        def getFileName(url,openUrl):
            if 'Content-Disposition' in openUrl.info():
                # If the response has Content-Disposition, try to get filename from it
                cd = dict(map(
                    lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                    openUrl.info().split(';')))
                if 'filename' in cd:
                    filename = cd['filename'].strip("\"'")
                    if filename: return filename
            # if no filename was found above, parse it out of the final URL.
            return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

        r = urllib2.urlopen(urllib2.Request(url))
        try:
            fileName = fileName or getFileName(url,r)
            with open(fileName, 'wb') as f:
                shutil.copyfileobj(r,f)
        finally:
            r.close()


class FTPDownloader(AbstractDownloader):
    def __init__(self):
        pass

class GITDownloader(AbstractDownloader):
    def __init__(self):
        pass

class SVNDownloader(AbstractDownloader):
    def __init__(self):
        pass

