#!/usr/bin/env python
#encoding: utf-8

import sys, os
from os.path import basename
import urllib2
import urlparse
import shutil
import subprocess

from relo.core.log import logger

def curl(url, path):
    command = "curl -L -# -o '%s' '%s'" % (path, url)
    logger.debug(command)
    subprocess.call(command, shell=True)

class AbstractDownloader(object):
    def __init__(self):
        pass
    def url2name(self, url):
        return basename(urlsplit(url)[2])
    def download(self, url, path, localFileName = None):
        pass

class HTTPDownloader(AbstractDownloader):
    def __init__(self):
        AbstractDownloader.__init__(self)
        pass
    def download(self, url, path, fileName = None):
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
            with open(os.path.join(path, fileName), 'wb') as f:
                shutil.copyfileobj(r,f)
        finally:
            r.close()


class FTPDownloader(AbstractDownloader):
    def __init__(self):
        AbstractDownloader.__init__(self)
        pass

class GITDownloader(AbstractDownloader):
    def __init__(self):
        AbstractDownloader.__init__(self)
        pass

class SVNDownloader(AbstractDownloader):
    def __init__(self):
        AbstractDownloader.__init__(self)
        pass

