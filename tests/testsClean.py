import gmane as g, importlib
dreload(g)
dloads=g.DownloadGmaneData('/.gmane2/')
#dloads.downloadListIDS()
#dloads.getDownloadedLists()
#dloads.correctFilenames()
dloads.cleanDownloadedLists()

