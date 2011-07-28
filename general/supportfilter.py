import os.path
import doctype

class supportFilter(object):
    def getFileType(self, itempath):
        """
        takes a path and returns a filetype
        """
        ext = os.path.splitext(itempath)[1]
        ext = ext.lstrip('.')
        return ext

    def filterList(self, fileList):
        filteredList = []
        for path in fileList:
            ext = self.getFileType(path)
            if ext in doctype.supported:
                filteredList.append(path)

        return filteredList