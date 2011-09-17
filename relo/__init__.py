from relo import core
from relo import doctype
from relo.core import manage

def get_version():
    return core.get_version()

class Relo:
    def __init__(self, debug=False, all=False, hidden=False, links=False, content=False, recursive=False,
                 doctype=None, directory='./', key=''):
        """
        Main Relo class
        """
        self.debug = debug
        self.all = all
        self.hidden = hidden
        self.links = links
        self.recursive = recursive
        self.doctype = doctype
        self.dir = directory
        self.key = key

        if content:
            self.type = "content Search"
        else:
            self.type = "fileName Search"

        print "Relo: version %s" % get_version()
        print "Verbose: " + str(bool(self.debug))
        print "All Files: " + str(bool(self.all))
        if self.doctype == None:
            print "Special Doctype: None"
        else:
            print "Special Doctype: " + (self.doctype)
        print "Hidden Files: " + str(bool(self.hidden))
        print "Symbolic Links: " + str(bool(self.links))
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
            self.total_size, self.fileList = core.recursiveListFiles(self.dir, self.hidden, self.links)
        else:
            print "Listing directory content..."
            self.total_size, self.fileList = core.listFiles(self.dir, self.hidden, self.links)
        print "Supported File Types: " + repr(doctype.__all__)

    def filter(self):
        if self.all:
            self.filteredList = self.fileList
        elif not self.doctype==None:
            self.filteredList = core.filterDocType(self.fileList, self.doctype)
        else:
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
        #print self.filteredList
        #print self.extList
        for item in self.filteredList:
            manager.start(item)
    def startName(self):
        core.fileNameSearch(self.fileList, self.key)