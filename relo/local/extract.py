#!/usr/bin/env python
# encoding: utf-8

import tarfile
import os
from relo.core.log import logger

def printprogress(percent):
   barlen = percent * 0.8
   print '\r' + '#' * int(barlen) + '-' * (80 - int(barlen)) + ' ' + str(percent) + '%'
   if complete == 100:
       logger.info('File complete')

class sudotarinfo(object):
    size = None

class TarFile(tarfile.TarFile):
    def __init__(self, name=None, mode="r", fileobj=None, format=None, tarinfo=None, dereference=None, ignore_zeros=None, encoding=None, errors=None, pax_headers=None, debug=None, errorlevel=None):
        self.__progresscallback = None
        tarfile.TarFile.__init__(self, name, mode, fileobj, format, tarinfo, dereference, ignore_zeros, encoding, errors, pax_headers, debug, errorlevel)
    def add(self, name, arcname=None, recursive=True, exclude=None, filter=None, progress=None):
        if progress is not None:
            progress(0)
            self.__progresscallback = progress
        return tarfile.TarFile.add(self, name, arcname, recursive, exclude, filter)
    def addfile(self, tarinfo, fileobj=None, progress=None):
        if progress is not None:
            progress(0)
            self.__progresscallback = progress
        if fileobj is not None:
            fileobj = filewrapper(fileobj, tarinfo, self.__progresscallback)
        result = tarfile.TarFile.addfile(self, tarinfo, fileobj)
        return result
    def extractall(self, path=".", members=None, progress=None):
        self.__progresscallback = None
        if progress is not None:
            original = self.fileobj
            try:
                stats = os.fstat(self.fileobj.fileno())
                sudoinfo = sudotarinfo()
                sudoinfo.size = stats.st_size
                self.fileobj = filewrapper(self.fileobj, sudoinfo, progress)
                self.__progresscallback = None
            except:
                self.fileobj = original
                self.__progresscallback = progress

        result = tarfile.TarFile.extractall(self, path, members)
        self.fileobj = original

        return result
    def extract(self, member, path="", progress=None):

        if progress is not None:
            progress(0)
            self.__progresscallback = progress

        result = tarfile.TarFile.extract(self, member, path)

        return result

    def extractfile(self, member, progress=None):
        if progress is not None:
            progress(0)
            self.__progresscallback = progress

        fileobj = tarfile.TarFile.extractfile(self, member)

        if fileobj is not None:
            fileobj = filewrapper(fileobj, member, self.__progresscallback)

        return fileobj

class filewrapper(object):
    def __init__(self, fileobj, tarinfo, progress):
        self._fileobj = fileobj

        self._size = tarinfo.size

        if self._size <= 0 or self._size is None:
            # Invalid size, we will not bother with the progress
            progress = None

        if progress is not None:
            progress(0)
        self._progress = progress
        self._lastprogress = 0

        self._totalread = 0

    def _updateprogress(self, length):
        if self._progress is not None:
            self._totalread += length

            progress = (self._totalread * 100) / self._size

            if self._lastprogress < progress <= 100:
                self._progress(progress)
                self._lastprogress = progress

    def read(self, size= -1):
        data = self._fileobj.read(size)

        self._updateprogress(len(data))

        return data

    def readline(self, size= -1):
        data = self._fileobj.readline(size)

        self._updateprogress(len(data))

        return data

    def __getattr__(self, name):
        return getattr(self._fileobj, name)

    def __del__(self):
        self._updateprogress(self._size - self._totalread)

open = TarFile.open