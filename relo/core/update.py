#!/usr/bin/env python
# encoding: utf-8

class AbstractUpdater(object):
	def __init__(self):
		localVersion = 0
		remoteVersion = 0
		pass
	def getLocalVersion(self):
		pass
	def getRemoteVersion(self):
		pass
	def executeUpdate(self):
		pass

class ReloUpdater(AbstractUpdater):
	"""
	Updates the relo library itself.
	"""
	def __init__(self):
		super.__init__()

class DocTypeUpdater(AbstractUpdater):
	"""
	Updates the doctype plugins that are used for local search.
	Own git repo for doctypes?!?
	"""
	def __init__(self):
		super.__init__()
		localDocTypeList = []
		remoteDocTypeList = []
	def getLocalList(self):
		"""
		Returns the local doctype plugins in list format.
		With the version number included
		[['pdf', 1.2],['txt', 2.1]]
		"""
		pass
	def getRemoteList(self):
		pass
	def getLocalVersion(self):
		pass
	def getRemoteVersion(self):
		pass

class ExtensionUpdater(AbstractUpdater):
	"""
	Updates relo's extensions.
	"""
	def __init__(self):
		super.__init__()

class BackendUpdater(AbstractUpdater):
    """
    Updates index backends
    """
    def __init__(self):
        super.__init__()