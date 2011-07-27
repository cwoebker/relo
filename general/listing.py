import os

def listFiles(rootDir, hidden):
    """
    list files in specified directory
    """
    total_size = 0
    for root, subFolders, files in os.walk(rootDir):
        subFolders[:] = [sub for sub in subFolders if not sub.startswith('.')]
        for file in files:
            if file.startswith('.') and hidden==0:
                continue
            itempath = os.path.join(root, file)
            total_size += os.path.getsize(itempath)

    print "\nTotal Size:", str(total_size)