import gmane as g, os, pickle, time, numpy as n, nltk as k, sys
# ENV=os.environ["PATH"]
# import  importlib
# from IPython.lib.deepreload import reload as dreload
# importlib.reload(g.pca)
# importlib.reload(g.loadMessages)
# importlib.reload(g.listDataStructures)
# importlib.reload(g.textUtils)
# importlib.reload(g.tableHelpers)
# dreload(g,exclude="pytz")
# os.environ["PATH"]=ENV

TT=time.time()
#print("{0:.2f}".format(T.time()-TT)); TT=T.time()
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject

# dl=g.DownloadGmaneData('~/.gmane3/')
basedir = '/home/r/backup/gmane/'
# dl=g.DownloadGmaneData(basedir)
# dl.downloadedStats()
PDIR="pickledir/"
# pDump(dl,"{}dl.pickle".format(PDIR))
dl=pRead("{}dl.pickle".format(PDIR))
 
# lids=[i[0] for i in dl.lists[:20]][3:] # as 20 com maior numero de mensagens
# lids=[i[0] for i in dl.lists[:20]][5:25] # as 20 com maior numero de mensagens
lids=[i[0] for i in dl.lists[12:32]] # as 20 com maior numero de mensagens
lids=[i[0] for i in dl.lists[21:25]] # as 20 com maior numero de mensagens
lids=[i[0] for i in dl.lists[5:30]] # as 20 com maior numero de mensagens
TOTAL=1000
TDIR="/home/r/repos/artigoTextoNasRedes3/tables/SI/"
FDIR="/home/r/repos/artigoTextoNasRedes3/figs/SI/"
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,0,5)
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,0,5,basedir=basedir)

print("\n\nFEITAS TODAS AS ANALISES COM 1000 mensagens\n\n")

TOTAL=2000
TDIR="/home/r/repos/artigoTextoNasRedes3/tables/SI2/"
FDIR="/home/r/repos/artigoTextoNasRedes3/figs/SI2/"
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=1000,basedir=basedir)
