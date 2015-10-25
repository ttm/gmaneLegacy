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

from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(["I'd like an apple",
                            "An apple a day keeps the doctor away",
                            "Never compare an apple to an orange",
                            "I prefer scikit-learn to Orange"])
aa=(tfidf * tfidf.T).A
texts=[ds.messages[i][-1] for i in ds.message_ids]

tfidf = vect.fit_transform(texts)
bb=(tfidf * tfidf.T).A
check("made sims")

# ver se os autores que possuem mensagens com alta similaridade
# se eles se comunicam sempre ou não ou se tem de tudo.
# hipótese: tendem a se aliar ou competir, de forma
# que ou se comunicam com frequência ou não se comunicam

# verificar se as mensagens e respostas possuem
# maior similaridade entre si que outros pares de mensagens

# verificar se os indivíduos que mais se comunicam
# mantém similaridade mais alta
# mesmo em mensagens que não são trocadas entre os participantes

# ver incidencia das raizes "abstraction" e "entity" para as arvores taxonomicas
# ver incidencia dos synsets logo apos estas duas raizes

# ver reincidencia da arvore taxonomica
# e/ou de palavras relacionadas por meronimia e holonimia

# ver tamanho das cadeias ateh a raiz
# ver numero de caminhos ateh a raiz
# número medio e desvio de hiponimos de cada termo
# número médio e desvio dos primeiros hiperonimos de cada termo

# cruzando todos os termos com relação ao common_hyperyms
# a média de número de iperônimos comuns dá uma medida
# do quão focada e redundante é a mensagem ou o corpus todo.

# algum tipo de sentiment analysis





#array([[ 1.        ,  0.25082859,  0.39482963,  0.        ],
#       [ 0.25082859,  1.        ,  0.22057609,  0.        ],
#       [ 0.39482963,  0.22057609,  1.        ,  0.26264139],
#       [ 0.        ,  0.        ,  0.26264139,  1.        ]])

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

