
class fileHandler(object):
    def __init__(self):
        pass
    def fopen(self, itempath):
        self.fobj = open(itempath, "r")
        return fobj

    def readall(self):
        content = ""
        for line in fobj:
            content += line
        print content
        return content