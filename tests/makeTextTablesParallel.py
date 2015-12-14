import gmane as g, pickle, time, os, shutil
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
#dl=g.DownloadGmaneData('/disco/.gmane/')
#dl.downloadedStats()
#pDump(dl,"{}dl.pickle".format(PDIR))
dl=pRead("{}dl.pickle".format(PDIR))
#sys.exit()
dtags="",2,5,10,20
Totals=1000,2000,5000,10000,20000
#offsets=2000,4000,7000,13000.23000
offsets=12000,14000,17000,23000,33000
#Totals=20000,10000,5000,2000,1000
#offsets=3000,10000,13000,3000,3000
#dl=pRead("{}dl.pickle".format(PDIR))
TDIR="/root/repos/artigoTextoNasRedes/tables/SI{}/"
FDIR="/root/repos/artigoTextoNasRedes/figs/SI/"
tdir=[TDIR.format(ttag) for ttag in dtags]
fdir=[FDIR.format(ttag) for ttag in dtags]
if 1:
 for tt in tdir+fdir:
     if os.path.isdir(tt):
         shutil.rmtree(tt)
     os.mkdir(tt)

lids_=[[i[0] for i in dl.lists[:xx]] for xx in [10,20,30,40,50]] # as 20 com maior numero de mensagens
targs=[]
countstep=0
for lids in lids_: # para cada tamanho de snapshot
    countlist=0
    for lid in lids_:
        targs+=[(lid,Totals[countstep],tdir[countstep],fdir[countstep],None,offsets[countstep],0,"/disco/.gmane/")]
        countlist+=1
    countstep+=1
#    for lid in lids: # para cada lista do snapshot
    
import multiprocessing as mp
pool=mp.Pool(processes=5)
results__=[pool.apply_async(g.textUtils.makeTables_,targ) for targ in targs]
#results__=[pool.apply_async(g.textUtils.makeTables_,x) for x in list(zip(lids_,Totals,tdir,fdir,[None]*5,offsets,[0]*5,["/disco/.gmane/"]*5))]
output=[p.get() for p in results__]

#results__=[pool.apply_async(dl.downloadListMessages,args=x) for x in args_]
#TOTAL=1000
#lids=[i[0] for i in dl.lists[:20]] # as 20 com maior numero de mensagens
#TDIR="/root/repos/artigoTextoNasRedes/tables/SI/"
#FDIR="/root/repos/artigoTextoNasRedes/figs/SI/"
##g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,0,5)
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,2000,5)
#
#check("FEITAS TODAS AS ANALISES COM !000 mensagens")
#
#TOTAL=2000
#TDIR="/root/repos/artigoTextoNasRedes/tables/SI2/"
#FDIR="/root/repos/artigoTextoNasRedes/figs/SI2/"
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=3000)
#
#TOTAL=5000
#TDIR="/root/repos/artigoTextoNasRedes/tables/SI5/"
#FDIR="/root/repos/artigoTextoNasRedes/figs/SI5/"
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=6000)
#
#
#TOTAL=10000
#TDIR="/root/repos/artigoTextoNasRedes/tables/SI10/"
#FDIR="/root/repos/artigoTextoNasRedes/figs/SI10/"
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=11000)
#
#TOTAL=20000
#TDIR="/root/repos/artigoTextoNasRedes/tables/SI20/"
#FDIR="/root/repos/artigoTextoNasRedes/figs/SI20/"
#g.textUtils.makeTables_(lids,TOTAL,TDIR,FDIR,offset=21000)
#




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

