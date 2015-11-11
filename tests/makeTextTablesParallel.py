import gmane as g, pickle, time, os
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
# , os, pickle, time, numpy as n, nltk as k, sys
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
##importlib.reload(g.pca)
##importlib.reload(g.loadMessages)
##importlib.reload(g.listDataStructures)
importlib.reload(g.textUtils)
importlib.reload(g.tableHelpers)
importlib.reload(g.listDataStructures)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV
check("preambule1")
#print("{0:.2f}".format(T.time()-TT)); TT=T.time()
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject
PDIR="pickledir/"
#dl=g.DownloadGmaneData('~/.gmane3/')
dl=g.DownloadGmaneData('/data/.gmane/')
dl.downloadedStats()
pDump(dl,"{}dl.pickle".format(PDIR))
#dl=pRead("{}dl.pickle".format(PDIR))


dl=pRead("{}dl.pickle".format(PDIR))
TOTAL=1000
lids=[i[0] for i in dl.lists[:20]] # as 20 com maior numero de mensagens
TDIR="/root/repos/artigoTextoNasRedes/tables/SI/"
FDIR="/root/repos/artigoTextoNasRedes/figs/SI/"
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,0,5)
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,2000,5)

check("FEITAS TODAS AS ANALISES COM !000 mensagens")

TOTAL=2000
TDIR="/root/repos/artigoTextoNasRedes/tables/SI2/"
FDIR="/root/repos/artigoTextoNasRedes/figs/SI2/"
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=3000)

TOTAL=5000
TDIR="/root/repos/artigoTextoNasRedes/tables/SI5/"
FDIR="/root/repos/artigoTextoNasRedes/figs/SI5/"
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=6000)


TOTAL=10000
TDIR="/root/repos/artigoTextoNasRedes/tables/SI10/"
FDIR="/root/repos/artigoTextoNasRedes/figs/SI10/"
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=11000)

TOTAL=20000
TDIR="/root/repos/artigoTextoNasRedes/tables/SI20/"
FDIR="/root/repos/artigoTextoNasRedes/figs/SI20/"
g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=21000)





# colocar nas distancias ks,
# leitura por mensagens: de uso de verbos
# a cada 100 tokens
# e tamanho de msgs em caracteres



# implementar start from para pular os vdicts que já estiverem
# prontos.
# verificar quais redes são em ingles, talvez fazer já um identificador


#ipdb> f=open(tfilename,"wb"); pickle.dump(tobject["es"],f); f.close()
#*** TypeError: cannot serialize '_io.BufferedRandom' object
#ipdb> f=open(tfilename,"wb"); pickle.dump(tobject["sent_measures"],f); f.close()
#ipdb> f=open(tfilename,"wb"); pickle.dump(tobject["wn_"],f); f.close()
#wn_measures       wn_measures2_pos  
#ipdb> f=open(tfilename,"wb"); pickle.dump(tobject["wn_measures"],f); f.close()
#^[[A^[[D*** TypeError: cannot serialize '_io.BufferedReader' object
#    ipdb> f=open(tfilename,"wb"); pickle.dump(tobject["wn_measures2_pos"],f); f.close()
#    *** TypeError: cannot serialize '_io.BufferedReader' object

