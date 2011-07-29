from plugnplay import Interface

class DocType(Interface):
    """""
    Implements different type of docs
    """""
    def open(self, path):
        pass
    def search(self, key):
        pass
    def finish(self):
        pass