import gmane as g, importlib
dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadListIDS()
#dl.getDownloadedLists()
#dl.correctFilenames()
dl.cleanDownloadedLists()

