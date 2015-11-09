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

#char_measures=g.textUtils.medidasLetras_(ts); check("medidas letras")
#g.textUtils.makeCharTable(char_measures,TDIR)
#
#tok_measures=g.textUtils.medidasTokens__(ts,ncontractions); check("medidas tokens")
#g.textUtils.makeTokensTable(tok_measures,TDIR)
#g.textUtils.makeTokenSizesTable(tok_measures,TDIR)
##g.textUtils.makeTokenSizesTable(tok_measures,TDIR)
#g.tableHelpers.vstackTables(TDIR+"tokensInline_",TDIR+"tokenSizesInline_",TDIR+"tokensMergedInline")
#
sent_measures=g.textUtils.medidasSentencas_(ts); check("medidas sentenças")
#g.textUtils.makeSentencesTable(sent_measures,TDIR)
#
#msg_measures=g.textUtils.medidasMensagens_(ds,msg_ids); check("medidas mensagens")
#g.textUtils.makeMessagesTable(msg_measures,TDIR)
#
pos_measures=g.textUtils.medidasPOS_([i["tokens_sentences"] for i in sent_measures]); check("medidas POS")
#g.textUtils.makePOSTable(pos_measures,TDIR)
#
#wn_measures=g.textUtils.medidasWordnet_([i["tags"] for i in pos_measures]); check("medidas wordnet")
#g.textUtils.makeWordnetPOSTable(wn_measures,TDIR ) # medias e desvios das incidencias dos atributos
#
#wn_measures2_pos=g.textUtils.medidasWordnet2_POS(wn_measures); check("medidas wordnet 2")
#g.textUtils.makeWordnetTables2_POS(wn_measures2_pos,TDIR) # escreve arquivo com todas as 5 tabelas para cada pos

sinais=g.textUtils.medidasSinais_(ts)
dists=g.textUtils.ksAll(sinais,mkeys=["lens_tok","lens_word","lens_sent"])
g.textUtils.makeKSTables(dists,
        fnames=("ksTokens","ksWords","ksSents"),
        tags=("size of tokens","size of known words","size of sentences"))

sinais2=g.textUtils.medidasSinais2_(pos_measures)
dists2=g.textUtils.ksAll(sinais2,mkeys=["adj","sub","pun"])
g.textUtils.makeKSTables(dists2,
        fnames=("ksAdjs","ksSubs","ksPuns"),
        tags=("use of adjectives on sentences","use of substantives on sentences","use of punctuations on sentences"))

# correlação pierson e spearman (tem necessidade das duas?)
# pearson pegamos pelo PCA:
# 1) fazer as medidas para cada participante
nm=es.structs[4]
textosP=g.textUtils.textosParticipante(ds)
medidasP=g.textUtils.medidasParticipante(textosP)
# 2) vincular aas medidas da rede:
medidas=g.textUtils.medidasPCA(medidasP,nm)
# relaciona com cada setor para
# tirar a correlação e PCA
mvars=("clustering","degree","strength","Mpuncts_sents","Spuncts_sents","Mknownw_sents","Sknownw_sents","Mstopw_sents","Sstopw_sents")
mpca=g.textUtils.tPCA(medidas,mvars)
# escolher algumas medidas a mais
# fazer tabela com todas a correlacoes maiores que ?
# plotar para os setores diferentes?

# fazer pca com mais medidas
# fazer para os setores?





# terminar de fazer o pca



# jogar tudo no SI para varias listas
# fazer tabelas com medias gerais das medidas, dentre todas as listas

# colocar resultados principais no documento principal,
# com os textos perfeitos










