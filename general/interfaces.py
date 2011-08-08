from yapsy.IPlugin import IPlugin

class DocType(IPlugin):
    """""
    Implements different type of docs
    """""
    name = ""
    sname = ""
    def id(self):
        return  self.sname
    def meta(self):
        return self.name
    def load(self, path):
        pass
    def search(self, key):
        pass