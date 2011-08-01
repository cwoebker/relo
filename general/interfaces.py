from plugnplay import Interface

class DocType(Interface):
    """""
    Implements different type of docs
    """""
    def load(self, path):
        pass
    def search(self, key):
        pass