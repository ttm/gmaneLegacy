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

ts,ncontractions,msg_ids=g.textUtils.makeText_(ds,pr); check("make text")

char_measures=g.textUtils.medidasLetras_(ts); check("medidas letras")
g.textUtils.makeCharTable(char_measures,TDIR)

tok_measures=g.textUtils.medidasTokens__(ts,ncontractions); check("medidas tokens")
g.textUtils.makeTokensTable(tok_measures,TDIR)
g.textUtils.makeTokenSizesTable(tok_measures,TDIR)

sent_measures=g.textUtils.medidasSentencas_(ts); check("medidas sentenças")
g.textUtils.makeSentencesTable(sent_measures,TDIR)

msg_measures=g.textUtils.medidasMensagens_(ds,msg_ids); check("medidas mensagens")
g.textUtils.makeMessagesTable(msg_measures,TDIR)

pos_measures=g.textUtils.medidasPOS_([i["tokens_sentences"] for i in sent_measures]); check("medidas POS")
g.textUtils.makePOSTable(pos_measures,TDIR)

wn_measures=g.textUtils.medidasWordnet_([i["tags"] for i in pos_measures]); check("medidas wordnet")
wn_measures2=g.textUtils.medidasWordnet2_(wn_measures); check("medidas wordnet2")
g.textUtils.makeWordnetTable(wn_measures2,TDIR)



# 2 tabelas?
# uma com medidas de medias e desvios de hiperonimos e hiponimos, 
# outra com a maior incidencia das raizes
# fazer separado para as pos tags?
# sim.

# terminar de fazer o roteiro da analise com kolm e pca
# jogar tudo no SI para varias listas
# fazer tabelas com medias gerais das medidas, dentre todas as listas

# colocar resultados principais no documento principal,
# com os textos perfeitos










