import gmane as g, importlib
dreload(g)
dl=g.DownloadGmaneData('/.gmane2/')
dl.downloadListIDS()
dl.getDownloadedLists()
dl.correctFilenames()
dl.cleanDownloadedLists()

