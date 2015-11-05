import gmane as g, os, pickle, time, numpy as n, nltk as k, sys
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.pca)
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.textUtils)
importlib.reload(g.tableHelpers)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
#n.random.normal(0,1,1000000)
NA=10**3 # numero de amostras
ND=10**2 # numero de comparações de distribuições

alfas=[0.1,0.05,0.025,0.01,0.005,0.001]
calfas=[1.22,1.36,1.48,1.63,1.73,1.95]

##########3
## comparing words from literary works
l1F=k.corpus.gutenberg.words("shakespeare-hamlet.txt")
l2F=k.corpus.gutenberg.words("bible-kjv.txt")
l3F=k.corpus.gutenberg.words("melville-moby_dick.txt")
l4F=k.corpus.machado.words("romance/marm09.txt") # memorias postumas
lF=[l1F,l2F,l3F,l4F]
llF=[len(i) for i in lF]

l1S=k.corpus.gutenberg.sents("shakespeare-hamlet.txt")
l2S=k.corpus.gutenberg.sents("bible-kjv.txt")
l3S=k.corpus.gutenberg.sents("melville-moby_dick.txt")
l4S=  k.corpus.machado.sents("romance/marm05.txt") # memorias postumas
lS=[l1S,l2S,l3S,l4S]
llS=[len(i) for i in lS]



l1=k.corpus.gutenberg.raw("shakespeare-hamlet.txt")
l2=k.corpus.gutenberg.raw("bible-kjv.txt")
l3=k.corpus.gutenberg.raw("melville-moby_dick.txt")
l4=  k.corpus.machado.raw("romance/marm05.txt") # memorias postumas

l=[l1,l2,l3,l4]
ll=[len(i) for i in l]
print(ll)
## mede uso de tokens e sentencas do meio de cada corpus.

l_=[i[int(j*.15):int(j*.85)] for i,j in zip(l,ll)]
ll_=[len(i) for i in l_]
l1_=[i[:int(j*.5)] for i,j in zip(l_,ll_)]
l2_=[i[int(j*.5):] for i,j in zip(l_,ll_)]
print(ll_)

# medidas para um dos casos
NE=1000 # número de eventos na amostra
texto=l1_[0]
NC=len(texto)//NE # número de caracteres no evento
textos=[texto[j*NC:(j+1)*NC] for j in range(NE)]
med=[g.medidasTokens(i) for i in textos]
med_=[g.medidasTamanhosTokens(i) for i in med]
sinal1=[i["mkw"] for i in med_]
sinal1b=[i["dkw"] for i in med_]
sinal2=[i["msw"] for i in med_]
sinal2b=[i["dsw"] for i in med_]

texto2=l2_[0]
NC=len(texto2)//NE # número de caracteres no evento
textos2=[texto2[j*NC:(j+1)*NC] for j in range(NE)]
med2=[g.medidasTokens(i) for i in textos2]
med2_=[g.medidasTamanhosTokens(i) for i in med2]
sinal21 =[i["mkw"] for i in  med2_]
sinal21b=[i["dkw"] for i in med2_]
sinal22 =[i["msw"] for i in  med2_]
sinal22b=[i["dsw"] for i in med2_]

texto3=l1_[1]
NC=len(texto3)//NE # número de caracteres no evento
textos3=[texto3[j*NC:(j+1)*NC] for j in range(NE)]
med3=[g.medidasTokens(i) for i in textos3]
med3_=[g.medidasTamanhosTokens(i) for i in med3]
sinal31 =[i["mkw"] for i in  med3_]
sinal31b=[i["dkw"] for i in  med3_]
sinal32 =[i["msw"] for i in  med3_]
sinal32b=[i["dsw"] for i in  med3_]

#print(g.kolmogorovSmirnovDistance(sinal1,sinal2),
#g.kolmogorovSmirnovDistance(sinal1,sinal21),
#g.kolmogorovSmirnovDistance(sinal1,sinal31),
#)

# renderiza tabelinha com caracteristicas gerais de cada
# texto total.
labels=("H,H1,H2","B,B1,B2","M,M1,M2",r"E,E1,E2")
labelsh=("label","description","chars","tokens","sentences",
        r"$|kw|$", r"$\mu(kw)$",r"$\sigma(kw)$",
        r"$|sw|$", r"$\mu(sw)$",r"$\sigma(sw)$")
textos3=l_
med3=[g.medidasTokens(i) for i in textos3]
med3_=[g.medidasTamanhosTokens(i) for i in med3]
sinal31_ =[len(i["kw"]) for i in  med3]
sinal31 =[i["mkw"] for i in  med3_]
sinal31b=[i["dkw"] for i in  med3_]
sinal32_ =[len(i["sw"]) for i in  med3]
sinal32 =[i["msw"] for i in  med3_]
sinal32b=[i["dsw"] for i in  med3_]
data=[["Hamlet by Shakespeare","King James Version of the Holly Bible", "Moby Dick by Herman Melville",r"Esa\'u e Jac\'o from Machado de Assis"]]
data+=[ll]
data+=[llF]
data+=[llS]
data+=[sinal31_,sinal31,sinal31b,sinal32_,sinal32,sinal32b]
#data_=list(zip(data))
data_=[[i[j] for i in data] for j in range(4)]
caption="""General description of the texts used to exemplify the use of the $c$ statistic.
Individual values of number of characters, tokens, sentences give context.
Mean and standard deviation of the size of known words $kw$ and of the stopwords
$st$ are used in next tables.
Numbers in the labels indicate first and second half of the corresponding text in the next tables."""
fname="textsGeneral.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"textsGeneral")

# renderiza tabelinha com todos os 12 textos as distâncias


# parte para análise de som

# depois do estado do SO
check("antes")
def medidas(texto):
    sinal=g.medidasTokensQ_(texto)
    sinal1_,sinal2_=sinal["kw"],sinal["sw"]

    check("MED antes")
    NE=1000 # número de eventos na amostra
    NC=len(texto)//NE # número de caracteres no evento
    textos=[texto[j*NC:(j+1)*NC] for j in range(NE)]
    med=[g.medidasTokensQ(i) for i in textos]
#    med_=[g.medidasTamanhosTokens(i) for i in med]
    sinal1=[i["mkw"] for i in  med]
    sinal1b=[i["dkw"] for i in med]
    sinal2=[i["msw"] for i in  med]
    sinal2b=[i["dsw"] for i in med]
    check("MED fim")
    return sinal1,sinal1b,sinal2,sinal2b,sinal1_,sinal2_

#LL=[i[j] for i in (l_,l1_,l2_) for j in range(4)]
#LL=[i for j in (l_,l1_,l2_) for i in j]
#LL=l_+l1_+l2_
LL=[]
for i in range(len(l_)):
    LL+=[l_[i],l1_[i],l2_[i]]
todas_medidas=[medidas(i) for i in LL]
check("fim")

# fazer distancia de KS para cada par
data=[]
data2=[]
for i in range(12):
    data.append([])
    data2.append([])
    for j in range(12):
        ksd=g.kolmogorovSmirnovDistance_(
                   todas_medidas[i][0],todas_medidas[j][0])
        data[-1].append( ksd[0] )
        data2[-1].append( ksd[2] )
labels=( "H","H1","H2","B","B1","B2","M","M1","M2","E","E1","E2")
labels_=[(l,"") for l in labels]
labels__=[i for j in labels_ for i in j]
data_=[(i,j) for i,j in zip(data,data2)]
data__=[i for j in data_ for i in j]
labelsh=("", "H","H1","H2","B","B1","B2","M","M1","M2","E","E1","E2")
fname="textsDistances.tex"
caption=r"Values of $c$ for histograms drawn from mean of the sizes of the known words."
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"textsDistances")

data=[]
data2=[]
for i in range(12):
    data.append([])
    data2.append([])
    for j in range(12):
        ksd=g.kolmogorovSmirnovDistance_(
                   todas_medidas[i][1],todas_medidas[j][1])
        data[-1].append(ksd[0] )
        data2[-1].append(ksd[2] )
data_=[(i,j) for i,j in zip(data,data2)]
data__=[i for j in data_ for i in j]
fname="textsDistances2.tex"
caption=r"Values of $c'$ for histograms drawn from the standard deviation of the sizes of the known words."
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"textsDistances")


data=[]
data2=[]
for i in range(12):
    data.append([])
    data2.append([])
    for j in range(12):
        ksd=g.kolmogorovSmirnovDistance_(
                   todas_medidas[i][2],todas_medidas[j][2])
        data[-1].append(  ksd[0] )
        data2[-1].append( ksd[2] )
data_=[(i,j) for i,j in zip(data,data2)]
data__=[i for j in data_ for i in j]
fname="textsDistances3.tex"
caption=r"Values of $c'$ for histograms drawn from the mean of the sizes of the stopwords."
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"textsDistances")

data=[]
data2=[]
for i in range(12):
    data.append([])
    data2.append([])
    for j in range(12):
        ksd=g.kolmogorovSmirnovDistance_(
                   todas_medidas[i][3],todas_medidas[j][3]
                         )
        data[-1].append(  ksd[0] )
        data2[-1].append( ksd[2] )
data_=[(i,j) for i,j in zip(data,data2)]
data__=[i for j in data_ for i in j]
fname="textsDistances4.tex"
caption=r"Values of $c'$ for histograms drawn from the standard deviation of the sizes of the stopwords."
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"textsDistances")

data=[]
data2=[]
for i in range(12):
    data.append([])
    data2.append([])
    for j in range(12):
        ksd=g.kolmogorovSmirnovDistance_(
                   todas_medidas[i][4],todas_medidas[j][4] )
        data[-1].append( ksd[0] )
        data2[-1].append( ksd[2] )
data_=[(i,j) for i,j in zip(data,data2)]
data__=[i for j in data_ for i in j]
fname="textsDistances2b.tex"
caption=r"Values of $c'$ for histograms drawn from the sizes of the known words."
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"textsDistances")

data=[]
data2=[]
for i in range(12):
    data.append([])
    data2.append([])
    for j in range(12):
        ksd=g.kolmogorovSmirnovDistance_(
                   todas_medidas[i][5],todas_medidas[j][5])
        data[-1].append( ksd[0] )
        data2[-1].append( ksd[2] )
data_=[(i,j) for i,j in zip(data,data2)]
data__=[i for j in data_ for i in j]
fname="textsDistances4b.tex"
caption=r"Values of $c'$ for histograms drawn from sizes of the stopwords."
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"textsDistances")


