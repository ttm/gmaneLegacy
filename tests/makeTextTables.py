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

import gmaneLegacy as g, os, pickle, time as T, numpy as n
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
TOTAL_M=200
dss=[]; iNs=[]; nms=[]; tss=[]; nps=[]
PDIR="pickledir/"
for lid in dl.lists[4:6]:
    lid=lid[0]
    print("\n",lid)
#    label=labels[lid]
    lm=g.LoadMessages(lid,TOTAL_M,basedir="~/.gmane3/")
    print(lid+"{0:.2f} for loading messages".format(T.time()-TT)); TT=T.time()
    ds=g.ListDataStructures(lm,text="yes")

    print(lid+"{0:.2f} for data structures".format(T.time()-TT)); TT=T.time()
    dss.append(ds)
    pDump(ds,"{}ds{}.pickle".format(PDIR,lid))

    ts=g.TimeStatistics(ds)
    print("{0:.2f} for statistics along time".format(T.time()-TT)); TT=T.time()
    tss.append(ts)
    pDump(ts,"{}ts{}.pickle".format(PDIR,lid))

    iN=g.InteractionNetwork(ds)
    print("made interaction network")
    iNs.append(iN)
    pDump(iN,"{}iN{}.pickle".format(PDIR,lid))

    nm=g.NetworkMeasures(iN,exclude=["rich_club"])
    print("network mesaures")
    nms.append(nm)
    pDump(nm,"{}nm{}.pickle".format(PDIR,lid))

    np2_=g.NetworkPartitioning(nm,2,"g")
    print("partitioned network")
    nps.append(np2_)
    pDump(nm,"{}np{}.pickle".format(PDIR,lid))

data_=[]; count=0
for lid in dl.lists[4:6]:
    lid=lid[0]
    ds=dss[count]; np=nps[count];  count+=1
    date1=ds.messages[ds.message_ids[0]][2].isoformat().split("T")[0]
    date2=ds.messages[ds.message_ids[-1]][2].isoformat().split("T")[0]
    N=ds.n_authors
    Ns=[len(i) for i in np.sectorialized_agents__]
    Ns_=[100*len(i)/N for i in np.sectorialized_agents__]
    M_=TOTAL_M-ds.n_messages
    Mh=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[2]])
    Mi=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[1]])
    Mp=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[0]])
    M=[Mh,Mi,Mp][::-1]
    M2=[100*i/ds.n_messages for i in M]
    MN=M_/N
    MN_=[i/j if j!=0 else n.inf for i,j in zip(M,Ns)]
    idsh=[i[0] for j in np.sectorialized_agents__[2] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    idsi=[i[0] for j in np.sectorialized_agents__[1] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    idsp=[i[0] for j in np.sectorialized_agents__[0] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    idsh_=len(idsh)
    idsi_=len(idsi)
    idsp_=len(idsp)
    ids=[idsh_,idsi_,idsp_][::-1]
    Gamma=len([i for i in ds.message_ids if ds.messages[i][1]==None])
    ids_=[100*ii/Gamma for ii in ids]
    print(sum(ids),Gamma)
    data_.append([date1,date2,N,Ns,Ns_,M,M2,Gamma,ids,ids_,M_,MN,MN_])

#tstring=g.makeTables(labels_,data_)
#print(tstring)
#TDIR="tables/"
#TDIR="/home/r/repos/stabilityInteraction/tables/"
#FDIR="figs/"
#print(label+"{0:.2f} for making overall table".format(T.time()-TT)); TT=T.time()
#
##g.writeTex(tstring,TDIR+"tab1Geral.tex")
#

