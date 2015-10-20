# file dedicated to making the tables
# for the main document and the Supporting Information
# of the artigcle about text differentiation:
# https://github.com/ttm/artigoTextoNasRedes/ AND
# http://arxiv.org/abs/1412.7309

# tentar fazer as tabelas focadas nas medidas?

# fazer td com 100 mensagens somente de cada lista

# fazer tabela geral só com CPP
# incluir mensagens/ano na tabela
# tirar as datas para a tabela no corpo do artigo

# tentar paralelizar

# fazer tabela de caracteres soh com LAD
# para o corpo do artigo.
# renderizar 4 listas
# avaliar fazer para mais listas para tirar médias e desvios

import gmane as g, os, pickle, time as T, numpy as n
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.pca)
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

TT=T.time()
#print("{0:.2f}".format(T.time()-TT)); TT=T.time()
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject

#dl=g.DownloadGmaneData('~/.gmane3/')
#dl.downloadedStats()
PDIR="pickledir/"
#pDump(dl,"{}dl.pickle".format(PDIR))
dl=pRead("{}dl.pickle".format(PDIR))

###### DATA STRUCTURES
dss=[]; iNs=[]; nms=[]; tss=[]; nps=[]
PDIR="pickledir/"
for lid in dl.lists[:4]:
    lid=lid[0]
    print("\n",lid)
#    label=labels[lid]
    lm=g.LoadMessages(lid,500,basedir="~/.gmane3/")
    print(lid+"{0:.2f} for loading messages".format(T.time()-TT)); TT=T.time()
    ds=g.ListDataStructures(lm,text="yes")
    print(lid+"{0:.2f} for data structures".format(T.time()-TT)); TT=T.time()
    pDump(ds,"{}ds{}.pickle".format(PDIR,lid))
    dss.append(ds)

    ts=g.TimeStatistics(ds)
    print("{0:.2f} for statistics along time".format(T.time()-TT)); TT=T.time()
    pDump(ts,"{}ts{}.pickle".format(PDIR,lid))
    tss.append(ts)

    iN=g.InteractionNetwork(ds)
    print("made interaction network")
    iNs.append(iN)
    nm=g.NetworkMeasures(iN,exclude=["rich_club"])
    print("network mesaures")
    nms.append(nm)
    np2_=g.NetworkPartitioning(nm,2,"g")
    print("partitioned network")
    nps.append(np2_)


#for lid in dl.lists[:10]:
#    lid=lid[0]
#    tss.append(pRead("{}ts{}.pickle".format(PDIR,lid)))
#    print(lid+"{0:.2f} for PICKLE loading time statistics".format(T.time()-TT)); TT=T.time()


# Faz rede
# particiona rede
#for i in [0]:
#    labels_.append(labels[dl.downloaded_lists[i]])
data_=[]; count=0
for lid in dl.lists[:4]:
    lid=lid[0]
    ds=dss[count]; count+=1
    date1=ds.messages[ds.message_ids[0]][2].isoformat().split("T")[0]
    date2=ds.messages[ds.message_ids[-1]][2].isoformat().split("T")[0]
    N=ds.n_authors
    Gamma=len([i for i in ds.message_ids if ds.messages[i][1]==None])
    M_=20000-ds.n_messages
    data_.append([date1,date2,N,Gamma,M_])
#tstring=g.makeTables(labels_,data_)
#print(tstring)
#TDIR="tables/"
#TDIR="/home/r/repos/stabilityInteraction/tables/"
#FDIR="figs/"
#print(label+"{0:.2f} for making overall table".format(T.time()-TT)); TT=T.time()
#
##g.writeTex(tstring,TDIR+"tab1Geral.tex")
#

