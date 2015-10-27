import gmane as g, os, pickle, time, numpy as n, nltk as k, sys
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.pca)
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.utils)
importlib.reload(g.tableHelpers)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV
from pylatex import Document, Section, Subsection, Subsubsection, Table, Math, TikZ, Axis, \
            Plot, Figure, Package
from pylatex.utils import italic, escape_latex

TT=time.time()
s1=n.arange(10)
s2=n.arange(0,10,100)
dist=g.kolmogorovSmirnovDistance(s1,s2)
import pylab as p
s3=n.arange(20)
#p.plot(s1)
#p.plot(s3)
#p.show()
def testUniform(n1,n2):
    s1=n.random.random(n1)
    s2=n.random.random(n2)
    dist=g.kolmogorovSmirnovDistance(s1,s2)
    return dist

# fazer pdf como no poema de sonhos
# fazer 10000 simulacoes com 2 distribuicoes iguais:
dists=[]
dists_=[]
# gaussianas

TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
#n.random.normal(0,1,1000000)
check("antes")
NA=10**3 # numero de amostras
ND=10**2 # numero de distribuicoes

# escolhe os c(\alpha), ve se temos menos casos que \alpha*ND
alfas=[0.1,0.05,0.025,0.01,0.005,0.001]
calfas=[1.22,1.36,1.48,1.63,1.73,1.95]

#dists=[g.kolmogorovSmirnovDistance(
#        n.random.normal(0,1,NA),n.random.normal(0,1,NA))
#        for i in range(ND)]
#check("normal")
#dists2=[g.kolmogorovSmirnovDistance(
#        n.random.normal(3,2,NA),n.random.normal(3,2,NA))
#        for i in range(ND)]
#check("normal")
#
#dists3=[g.kolmogorovSmirnovDistance(
#        n.random.normal(6,3,NA),n.random.normal(6,3,NA))
#        for i in range(ND)]
#check("normal")
#
#
#for alfa, calfa in zip(alfas,calfas):
#    print(sum([dist>calfa for dist in dists]), alfa*ND )
#print("\n")
#for alfa, calfa in zip(alfas,calfas):
#    print(sum([dist>calfa for dist in dists2]), alfa*ND )
#print("\n")
#for alfa, calfa in zip(alfas,calfas):
#    print(sum([dist>calfa for dist in dists3]), alfa*ND )
#check("normal")
#check("uniforme")
#distsU=[g.kolmogorovSmirnovDistance(
#        n.random.random(NA),n.random.random(NA))
#        for i in range(ND)]
#check("uniforme")
#distsU2=[g.kolmogorovSmirnovDistance(
#        2*n.random.random(NA)+2,2*n.random.random(NA)+2)
#        for i in range(ND)]
#check("uniforme")
#distsU3=[g.kolmogorovSmirnovDistance(
#        3*n.random.random(NA)+4,3*n.random.random(NA)+4)
#        for i in range(ND)]
#check("uniforme")
#for alfa, calfa in zip(alfas,calfas):
#    print(sum([dist>calfa for dist in distsU]), alfa*ND )
#    print(sum([dist>calfa for dist in distsU2]), alfa*ND )
#    print(sum([dist>calfa for dist in distsU3]), alfa*ND ,"\n")
#check("uniforme")
#check("weibull")
#distsW=[g.kolmogorovSmirnovDistance(
#        n.random.weibull(0.01,NA),n.random.weibull(0.01,NA))
#        for i in range(ND)]
#check("weibull")
#distsW2=[g.kolmogorovSmirnovDistance(
#        n.random.weibull(2.01,NA),n.random.weibull(2.01,NA))
#        for i in range(ND)]
#check("weibull")
#distsW3=[g.kolmogorovSmirnovDistance(
#        n.random.weibull(4.01,NA),n.random.weibull(4.01,NA))
#        for i in range(ND)]
#check("weibull")
#for alfa, calfa in zip(alfas,calfas):
#    print(sum([dist>calfa for dist in distsW]), alfa*ND )
#    print(sum([dist>calfa for dist in distsW2]), alfa*ND )
#    print(sum([dist>calfa for dist in distsW3]), alfa*ND,"\n" )
#check("weibull")
#
#############3
# feito até agora:
#### se as distribuições são iguais, os valores c(alfa) só ocorrem
#### com frequência máxima ~ alfa. Raros casos alcançaram alfa, quando o número de comparações era muito pequeno

############3
# fazer comparação de distribuições diferentes:

distsD=[g.kolmogorovSmirnovDistance(
        n.random.random(NA),2*n.random.random(NA)+2)
        for i in range(ND)]
check("diferenca")

distsD2=[g.kolmogorovSmirnovDistance(
        2*n.random.random(NA)+2,n.random.random(NA)+2)
        for i in range(ND)]
check("diferenca")

distsD3=[g.kolmogorovSmirnovDistance(
        2*n.random.random(NA),1*n.random.random(NA))
        for i in range(ND)]
# distances of same normal
check("diferenca")

for alfa, calfa in zip(alfas,calfas):
    print("encontrado: ", sum([dist>calfa for dist in distsD])/ND, alfa*ND  , n.mean(distsD),  n.std(distsD))
    print("encontrado: ", sum([dist>calfa for dist in distsD2])/ND, alfa*ND , n.mean(distsD2), n.std(distsD2))
    print("encontrado: ", sum([dist>calfa for dist in distsD3])/ND, alfa*ND , n.mean(distsD3), n.std(distsD3))
# 1000 comparacoes entre distribuições iguais

# medir media e desvio de c(alfa) para valores de (uniforme*x) com x em [1,2]
xx=n.linspace(.5,2,16,endpoint=True)
distsAll=[[g.kolmogorovSmirnovDistance(
        xxx*n.random.random(NA),n.random.random(NA)) for i in range(ND)]
        for xxx in xx]
distsAll_=[(n.mean(dd),n.std(dd)) for dd in distsAll]
i=0
for xxx in xx:
    print("right limit", xxx,distsAll_[i][0],distsAll_[i][1])
    # TABULAR TTM
    i+=1
check("diferencas uniformes")


xxN=n.linspace(.5,2,16,endpoint=True)
distsAllN=[[g.kolmogorovSmirnovDistance(
        n.random.normal(0,xxx,NA),n.random.normal(0,1,NA)) for i in range(ND)]
        for xxx in xxN]
distsAllN_=[(n.mean(dd),n.std(dd)) for dd in distsAllN]
i=0
for xxx in xxN:
    print("standards deviation", xxx,distsAllN_[i][0],distsAllN_[i][1])
    # TABULAR TTM
    i+=1
check("diferencas normais\n")

###
xxN2=n.linspace(0,1,11,endpoint=True)
distsAllN2=[[g.kolmogorovSmirnovDistance(
        n.random.normal(xxx,1,NA),n.random.normal(0,1,NA)) for i in range(ND)]
        for xxx in xxN2]
distsAllN2_=[(n.mean(dd),n.std(dd)) for dd in distsAllN2]
i=0
for xxx in xxN2:
    print("mean",xxx,distsAllN2_[i][0],distsAllN2_[i][1])
    # TABULAR TTM
    i+=1
check("diferencas normais -> 2\n")

check("diferencas weibull\n")
xxW=n.linspace(.1,2,20,endpoint=True)
distsAllW=[[g.kolmogorovSmirnovDistance(
        n.random.weibull(xxx,NA),n.random.weibull(1,NA)) for i in range(ND)]
        for xxx in xxW]
distsAllW_=[(n.mean(dd),n.std(dd)) for dd in distsAllW]
i=0
for xxx in xxW:
    print(xxx,distsAllW_[i][0],distsAllW_[i][1])
    # TABULAR TTM
    i+=1
check("diferencas weibull")

# valores maiores de amostras (diminui desvio padrao de c(alpha))
# e mais comparações (aumenta validade do resultado)

# os valores devem ser bem baixos para x=1 e atingir ~11,2 em x=2

# medir assim também para os distribuições gaussianas e weibull



#aa=[g.kolmogorovSmirnovDistance(n.random.normal(0,1,100),n.random.normal(0,1,100)) for i in range(1000)]


# fazer teste para comparar com número de amostras diferente

# medidas para textos do machado de assis
# para genesis em ptbr e em ingles

# escolher distribuições quaisquer






