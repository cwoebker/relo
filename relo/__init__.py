from relo import core
from relo import doctype
from relo.core import manage
from relo.core import log

def get_version():
    return core.get_version()

class Relo:
    def __init__(self, info=False, debug=False, all=False, hidden=False, links=False, filelog=False, content=False, recursive=False,
                 doctype=None, directory='./', key=''):
        """
        Main Relo class
        """
        self.info = info
        self.debug = debug
        self.all = all
        self.hidden = hidden
        self.links = links
        self.recursive = recursive
        self.doctype = doctype
        self.dir = directory
        self.key = key

        self.log = log.Logger(self.info, self.debug)

        if content:
            self.type = "content Search"
        else:
            self.type = "fileName Search"

        self.log.info("Relo: version %s" % get_version())
        if self.info:
            self.log.info("Mode: Info")
        elif self.debug:
            self.log.info("Mode: Debug")
        else:
            self.log.info("Mode: Normal")
        self.log.info("All Files: " + str(bool(self.all)))
        if self.doctype == None:
            self.log.info("Special DocType: None")
        else:
            self.log.info("Special DocType: " + (self.doctype))
        self.log.info("Hidden Files: " + str(bool(self.hidden)))
        self.log.info("Symbolic Links: " + str(bool(self.links)))
        self.log.info("Recursive: " + str(bool(self.recursive)))
        self.log.info("Search Type: " + self.type)
        self.log.info("Directory: " + self.dir)
        self.log.info("Searching for: " + self.key)

        self.filteredList = []
        self.extList = []
        self.total_size = 0
        self.fileList = []

    def list(self):
        if self.recursive:
            self.log.info("Listing directory content recursively...")
            self.total_size, self.fileList = core.recursiveListFiles(self.dir, self.hidden, self.links)
        else:
            self.log.info("Listing directory content...")
            self.total_size, self.fileList = core.listFiles(self.dir, self.hidden, self.links)
        self.log.debug("Supported File Types: " + repr(doctype.__all__))

    def filter(self):
        if self.all:
            self.filteredList = self.fileList
        elif not self.doctype==None:
            self.log.info("Selecting DocType files...")
            self.filteredList = core.filterDocType(self.fileList, self.doctype)
        else:
            self.log.info("Filtering file types...")
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