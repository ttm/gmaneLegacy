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
l1=k.corpus.gutenberg.words("shakespeare-hamlet.txt")
l2=k.corpus.gutenberg.words("bible-kjv.txt")
l3=k.corpus.gutenberg.words("melville-moby_dick.txt")
l4=k.corpus.machado.words("romance/marm05.txt") # memorias postumas

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








