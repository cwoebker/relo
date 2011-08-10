from relo import core
from relo import doctype
from relo.core import manage

def get_version():
    return core.get_version()

class Relo:
    def __init__(self, _debug=False, _hidden=False, _content=False, _recursive=False, _directory='./', _key=''):
        """
        Main Relo class
        """
        self.verbose = _debug
        self.hidden = _hidden
        self.recursive = _recursive
        self.dir = _directory
        self.key = _key

        if _content:
            self.type = "content Search"
        else:
            self.type = "fileName Search"

        print "Relo: version %s" % get_version()
        print "Verbose: " + str(bool(self.verbose))
        print "Hidden Files: " + str(bool(self.hidden))
        print "Recursive: " + str(bool(self.recursive))
        print "Search Type: " + self.type
        print "Directory: " + self.dir
        print "Searching for: " + self.key

        self.filteredList = []
        self.extList = []
        self.total_size = 0
        self.fileList = []

    def list(self):
        if self.recursive:
            print "Listing directory content recursively..."
            self.total_size, self.fileList = core.recursiveListFiles(self.dir, self.hidden)
        else:
            print "Listing directory content..."
            self.total_size, self.fileList = core.listFiles(self.dir, self.hidden)
        print "Supported File Types: " + repr(doctype.__all__)

    def filter(self):
        self.filteredList = core.filterList(self.fileList)
        for itempath in self.filteredList:
            item = core.getFileType(itempath)
            if item not in self.extList:
                self.extList.append(item)

    def start(self):
        if 'content' in self.type:
            self.startContent()
        else:
            self.startName()
    def startContent(self):
        manager = manage.Manager(self.key, self.extList)
        for item in self.filteredList:
            manager.start(item)
    def startName(self):
        core.fileNameSearch(self.fileList, self.key)