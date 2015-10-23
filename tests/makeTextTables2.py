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

import gmane as g, os, pickle, time, numpy as n, nltk as k
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.pca)
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.utils)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

TT=time.time()
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
TOTAL_M=100
dss=[]; iNs=[]; nms=[]; tss=[]; nps=[]
PDIR="pickledir/"
ES=[]
for lid in dl.lists[34:36]:
    lid=lid[0]
    es=g.EmailStructures(lid,TOTAL_M)
    ES.append(es)
#pDump(ES,"{}ES{}.pickle".format(PDIR,lid))

measures=[]; count=0
char_measures=[]
tok_measures=[]
size_measures=[]
sent_size_measures=[]
msg_size_measures=[]
pos_measures=[]
wordnet_measures=[]
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
for lid in dl.lists[34:36]:
    lid=lid[0]
    es=ES[count].structs; count+=1
    ds=es[1]; np=es[-1]
    measures.append(g.generalMeasures(ds,np))
    check("general measures")
    t=g.makeText(ds)[0]
    check("make text")
    char_measures.append(g.medidasLetras(t))
    check("char_measures")
    tok_measures.append(g.medidasTokens(t))
    check("tok measures")
    size_measures.append(g.medidasTamanhosTokens(tok_measures[-1]))
    check("size measures")
    sent_size_measures.append(g.medidasTamanhosSentencas(t,tok_measures[-1]))
    check("sent measures")
    msg_size_measures.append(g.medidasTamanhosMensagens(ds))
    check("msg size")
    pos_measures.append(g.medidasPOS(sent_size_measures[-1]["sTS"]))
    check("pos measures")
    wordnet_measures.append(g.medidasWordnet(tok_measures[-1]["kwss"]))
    check("wn measures")

#f=open("pickledir/brill_tagger3","rb")
#brill_tagger=pickle.load(f)
#f.close()
#
## POS TAGS
#aa=brill_tagger.tag(sent_size_measures[-1]["sTS"][0])

# faz uma tabela para o corpo do artigo
# tabela com 4 na sequência para o SI

# rotina para a tabela seguinte:
# conta 

#tstring=g.makeTables(labels_,data_)
#print(tstring)
#TDIR="tables/"
#TDIR="/home/r/repos/stabilityInteraction/tables/"
#FDIR="figs/"
#print(label+"{0:.2f} for making overall table".format(T.time()-TT)); TT=T.time()
#
##g.writeTex(tstring,TDIR+"tab1Geral.tex")
#

