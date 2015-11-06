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
dl=pRead("{}dl.pickle".format(PDIR))
TOTAL_M=100
#dss=[]; iNs=[]; nms=[]; tss=[]; nps=[]
ES=[]
check("antesAAAAAAAAAAAAA")
for lid in dl.lists[34:36]:
    lid=lid[0]
    es=g.EmailStructures(lid,TOTAL_M)
    ES.append(es)
check("depoisAAAAAAAAAAAA")
#pDump(ES,"{}ES{}.pickle".format(PDIR,lid))

es=ES[0]
ds=es.structs[1]
ts=es.structs[2]
pr=es.structs[-1]


#TDIR="/home/r/repos/stabilityInteraction/tables/"
TDIR="/home/r/repos/artigoTextoNasRedes/tables/"
gmeasures=g.generalMeasures(ds,pr,ts)
g.makeGeneralTable(gmeasures,TDIR)

#cmeasures=g.charsMeasures(ds,pr,ts)
#g.makeGeneralTable(cmeasures)

ts,ncontractions=g.textUtils.makeText_(ds,pr); check("make text")
char_measures=g.textUtils.medidasLetras_(ts); check("medidas letras")
g.textUtils.makeCharTable(char_measures,TDIR)

tok_measures=g.textUtils.medidasTokens__(ts,ncontractions); check("medidas letras")
g.textUtils.makeTokensTable(tok_measures,TDIR)

g.textUtils.makeTokenSizesTable(tok_measures,TDIR)



