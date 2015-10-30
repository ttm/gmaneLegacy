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

check("antes")
dists=[g.kolmogorovSmirnovDistance(
        n.random.normal(0,1,NA),n.random.normal(0,1,NA))
        for i in range(ND)]
check("normal1")
dists2=[g.kolmogorovSmirnovDistance(
        n.random.normal(3,2,NA),n.random.normal(3,2,NA))
        for i in range(ND)]
check("normal2")

dists3=[g.kolmogorovSmirnovDistance(
        n.random.normal(6,3,NA),n.random.normal(6,3,NA))
        for i in range(ND)]
check("normal3")
labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1'(\alpha)|$",r"$|C_2'(\alpha)|$",r"$|C_3'(\alpha)|$")
caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
of the null hypothesis for critical values of $\alpha$.
The number of comparisons is $N_c={}$,
each with the sample size of $N_o={}$ observations.
Each histogram have $N_b={}$ equally spaced bins.
The $N_o$ values of $c_1'$ were calculated using simulations of
 normal distributions with $\mu={}$ and $\sigma={}$.
The $N_o$ values of $c_2'$ were calculated using simulations of
 normal distributions with $\mu={}$ and $\sigma={}$.
The $N_o$ values of $c_3'$ were calculated using simulations of
 normal distributions with $\mu={}$ and $\sigma={}$.
Over all $N_c$ comparisons,
 $\mu(c_1')={:.4f}$ and $\sigma(c_1')={:.4f}$,
 $\mu(c_2')={:.4f}$ and $\sigma(c_2')={:.4f}$,
 $\mu(c_3')={:.4f}$ and $\sigma(c_3')={:.4f}$ .
""".format(ND,NA,30,
        0,1,
        3,2,
        6,3,
           n.mean(dists ),n.std(dists ),
           n.mean(dists2),n.std(dists2),
           n.mean(dists3),n.std(dists3),
           )


data=[]
labels=[]
for alfa, calfa in zip(alfas,calfas):
    n1=sum([dist>calfa for dist in dists])
    n2=sum([dist>calfa for dist in dists2])
    n3=sum([dist>calfa for dist in dists3])
    data.append((alfa,calfa,n1,n2,n3))
    labels.append(alfa*ND)
    print(n1, alfa*ND )
    print(sum([dist>calfa for dist in dists2]), alfa*ND )
    print(sum([dist>calfa for dist in dists3]), alfa*ND )
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
fname="tabNormNull.tex"
g.lTable(labels,labelsh,data,caption,TDIR+fname)

############
## Tabela Uniforme

check("antes")
dists=[g.kolmogorovSmirnovDistance(
        n.random.random(NA),n.random.random(NA))
        for i in range(ND)]
check("uniforme1")
dists2=[g.kolmogorovSmirnovDistance(
        2*n.random.random(NA)+2,2*n.random.random(NA)+2)
        for i in range(ND)]
check("uniforme2")

dists3=[g.kolmogorovSmirnovDistance(
        3*n.random.random(NA)+4,3*n.random.random(NA)+4)
        for i in range(ND)]
check("uniforme3")
labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1'(\alpha)|$",r"$|C_2'(\alpha)|$",r"$|C_3'(\alpha)|$")
caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
of the null hypothesis for critical values of $\alpha$.
The number of comparisons is $N_c={}$,
each with the sample size of $N_o={}$ observations.
Each histogram have $N_b={}$ equally spaced bins.
The $N_o$ values of $c_1'$ were calculated using simulations of
 uniform distributions within $[{},{})$.
The $N_o$ values of $c_2'$ were calculated using simulations of
 uniform distributions within $[{},{})$.
The $N_o$ values of $c_3'$ were calculated using simulations of
 normal distributions with $\mu={}$ and $\sigma={}$.
Over all $N_c$ comparisons,
 $\mu(c_1')={:.4f}$ and $\sigma(c_1')={:.4f}$,
 $\mu(c_2')={:.4f}$ and $\sigma(c_2')={:.4f}$,
 $\mu(c_3')={:.4f}$ and $\sigma(c_3')={:.4f}$ .
""".format(ND,NA,30,
        0,1,
        2,6,
        4,10,
           n.mean(dists ),n.std(dists ),
           n.mean(dists2),n.std(dists2),
           n.mean(dists3),n.std(dists3),
           )
data=[]
labels=[]
for alfa, calfa in zip(alfas,calfas):
    n1=sum([dist>calfa for dist in dists])
    n2=sum([dist>calfa for dist in dists2])
    n3=sum([dist>calfa for dist in dists3])
    data.append((alfa,calfa,n1,n2,n3))
    labels.append(alfa*ND)
    print(n1, alfa*ND )
    print(sum([dist>calfa for dist in dists2]), alfa*ND )
    print(sum([dist>calfa for dist in dists3]), alfa*ND )
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
fname="tabUniformNull.tex"
g.lTable(labels,labelsh,data,caption,TDIR+fname)



############
## Tabela Weibull

check("antes")
dists=[g.kolmogorovSmirnovDistance(
        n.random.weibull(0.1,NA),n.random.weibull(0.1,NA))
        for i in range(ND)]
check("weibull1")
dists2=[g.kolmogorovSmirnovDistance(
        n.random.weibull(2,NA),n.random.weibull(2,NA))
        for i in range(ND)]
check("weibull2")
dists3=[g.kolmogorovSmirnovDistance(
        n.random.weibull(4,NA),n.random.weibull(4,NA))
        for i in range(ND)]
check("weibull3")
dists4=[g.kolmogorovSmirnovDistance(
        n.random.weibull(6,NA),n.random.weibull(6,NA))
        for i in range(ND)]
check("weibull4")
labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1'(\alpha)|$",r"$|C_2'(\alpha)|$",r"$|C_3'(\alpha)|$",r"$|C_4'(\alpha)|$")
caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
of the null hypothesis for critical values of $\alpha$.
The number of comparisons is $N_c={}$,
each with the sample size of $N_o={}$ observations.
Each histogram have $N_b={}$ equally spaced bins.
The $N_o$ values of $c_1'$ were calculated using simulations of
 1-parameter Weibull distributions with $a={}$.
The $N_o$ values of $c_2'$ were calculated using simulations of
 1-parameter Weibull distributions with $a={}$.
The $N_o$ values of $c_3'$ were calculated using simulations of
 1-parameter Weibull distributions with $a={}$.
Over all $N_c$ comparisons,
The $N_o$ values of $c_4'$ were calculated using simulations of
 1-parameter Weibull distributions with $a={}$.
Over all $N_c$ comparisons,
 $\mu(c_1')={:.4f}$ and $\sigma(c_1')={:.4f}$,
 $\mu(c_2')={:.4f}$ and $\sigma(c_2')={:.4f}$,
 $\mu(c_3')={:.4f}$ and $\sigma(c_3')={:.4f}$ .
 $\mu(c_4')={:.4f}$ and $\sigma(c_4')={:.4f}$ .
""".format(ND,NA,30,
        0.1,
        2,
        4,
        6,
           n.mean(dists ),n.std(dists ),
           n.mean(dists2),n.std(dists2),
           n.mean(dists3),n.std(dists3),
           n.mean(dists4),n.std(dists4),
           )
data=[]
labels=[]
for alfa, calfa in zip(alfas,calfas):
    n1=sum([dist>calfa for dist in dists])
    n2=sum([dist>calfa for dist in dists2])
    n3=sum([dist>calfa for dist in dists3])
    n4=sum([dist>calfa for dist in dists4])
    data.append((alfa,calfa,n1,n2,n3,n4))
    labels.append(alfa*ND)
    print(n1, alfa*ND )
    print(sum([dist>calfa for dist in dists2]), alfa*ND )
    print(sum([dist>calfa for dist in dists3]), alfa*ND )
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
fname="tabWeibullNull.tex"
g.lTable(labels,labelsh,data,caption,TDIR+fname)


####################
# power function distribution

check("antes")
dists=[g.kolmogorovSmirnovDistance(
        n.random.power(0.3,NA),n.random.power(0.3,NA))
        for i in range(ND)]
check("power1")
dists2=[g.kolmogorovSmirnovDistance(
        n.random.power(1,NA),n.random.power(1,NA))
        for i in range(ND)]
check("power2")
dists3=[g.kolmogorovSmirnovDistance(
        n.random.power(2,NA),n.random.power(2,NA))
        for i in range(ND)]
check("power3")
dists4=[g.kolmogorovSmirnovDistance(
        n.random.power(3,NA),n.random.power(3,NA))
        for i in range(ND)]
check("weibull4")
dists4_=[g.kolmogorovSmirnovDistance(
        n.random.power(4,NA),n.random.power(4,NA))
        for i in range(ND)]
check("weibull4")

labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1'(\alpha)|$",r"$|C_2'(\alpha)|$",r"$|C_3'(\alpha)|$",r"$|C_4'(\alpha)|$",r"$|C_5'(\alpha)|$")
caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
of the null hypothesis for critical values of $\alpha$.
The number of comparisons is $N_c={}$,
each with the sample size of $N_o={}$ observations.
Each histogram have $N_b={}$ equally spaced bins.
The $N_o$ values of $c_1'$ were calculated using simulations of
 power functions distributions with $a={}$.
The $N_o$ values of $c_2'$ were calculated using simulations of
 power functions distributions with $a={}$.
The $N_o$ values of $c_3'$ were calculated using simulations of
 power functions distributions with $a={}$.
The $N_o$ values of $c_4'$ were calculated using simulations of
 power functions distributions with $a={}$.
The $N_o$ values of $c_5'$ were calculated using simulations of
 power functions distributions with $a={}$.
Over all $N_c$ comparisons,
 $\mu(c_1')={:.4f}$ and $\sigma(c_1')={:.4f}$,
 $\mu(c_2')={:.4f}$ and $\sigma(c_2')={:.4f}$,
 $\mu(c_3')={:.4f}$ and $\sigma(c_3')={:.4f}$ .
 $\mu(c_4')={:.4f}$ and $\sigma(c_4')={:.4f}$ .
 $\mu(c_5')={:.4f}$ and $\sigma(c_5')={:.4f}$ .
""".format(ND,NA,30,
        0.3,
        1,
        2,
        3,
        4,
           n.mean(dists ),n.std(dists ),
           n.mean(dists2),n.std(dists2),
           n.mean(dists3),n.std(dists3),
           n.mean(dists4),n.std(dists4),
           n.mean(dists4_),n.std(dists4_),
           )
data=[]
labels=[]
for alfa, calfa in zip(alfas,calfas):
    n1=sum([dist>calfa for dist in dists])
    n2=sum([dist>calfa for dist in dists2])
    n3=sum([dist>calfa for dist in dists3])
    n4=sum([dist>calfa for dist in dists4])
    n4_=sum([dist>calfa for dist in dists4_])
    data.append((alfa,calfa,n1,n2,n3,n4,n4_))
    labels.append(alfa*ND)
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
fname="tabPowerNull.tex"
g.lTable(labels,labelsh,data,caption,TDIR+fname)



###############3
#### medidas de diferenca

def min3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[:3]]
def max3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[-3:]]
xxN=n.linspace(.5,2,16,endpoint=True)
distsAllN=[[g.kolmogorovSmirnovDistance(
        n.random.normal(0,xxx,NA),n.random.normal(0,1,NA)) for i in range(ND)]
        for xxx in xxN]
distsAllN_=[(n.mean(dd),n.std(dd),n.median(dd),
    ("{:.3f},"*3)[:-1].format(*min3(dd)),
    ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllN]
i=0
labels=xxN
labelsh=[r"$\sigma$",r"$\mu(c')$",r"$\sigma(c')$","m(c')","min(c')","max(c')"]
#data=n.vstack((xxN,n.array(distsAllN_).T))
data=distsAllN_
caption=r"""Location and dispersion of $N_c={}$
measurements of $c'$ through simulations
with normal distributions and $N_o={}$ events each.
$N_b={}$ equal bins were used to make the histograms.
One normal distribution is fixed, with $\mu=0$ and $\sigma=1$,
and compared agaist normal distributions with $\mu=0$
and different values of $\sigma$.""".format(ND,NA, 30)
data_=[]
i=0
for dists in distsAllN:
    line=[]
    for calfa in calfas:
        line.append(sum([dist>calfa for dist in dists])/ND)
    data_.append(list(data[i])+line); i+=1

#labelsh=[r"$\sigma$"]+[r"$|C'({})|$".format(alfa) for alfa in alfas]
labelsh+=[r"$\overline{{C'({})}}$".format(alfa) for alfa in alfas]
#caption+=r"""Number of rejections of the null hypothesis for different values of $\alpha$."""
fname="tabNormDiff3.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"kolmDiff3")
        
#################
## segunda tabela de diferencas de distribuicoes normais
# variacao da media
xxN2=n.linspace(0,1,11,endpoint=True)
labels=xxN2
distsAllN2=[[g.kolmogorovSmirnovDistance(
        n.random.normal(xxx,1,NA),n.random.normal(0,1,NA)) for i in range(ND)]
        for xxx in xxN2]
data2=[(n.mean(dd),n.std(dd),n.median(dd),
    ("{:.3f},"*3)[:-1].format(*min3(dd)),
    ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllN2]
data2_=[]
i=0
for dists in distsAllN2:
    line=[]
    for calfa in calfas:
        line.append(sum([dist>calfa for dist in dists])/ND)
    data2_.append(list(data2[i])+line); i+=1
caption=r"""Location and dispersion of $N_c={}$
measurements of $c'$ through simulations
with normal distributions and $N_o={}$ events each.
$N_b={}$ equal bins were used to make the histograms.
One normal distribution is fixed, with $\mu=0$ and $\sigma=1$,
and compared agaist normal distributions with different values of $\mu$ and fixed $\sigma=1$.""".format(ND,NA, 30)

labelsh=[r"$\mu$",r"$\mu(c')$",r"$\sigma(c')$","m(c')","min(c')","max(c')"]
labelsh+=[r"$\overline{{C'({})}}$".format(alfa) for alfa in alfas]
fname="tabNormDiffMean.tex"
g.lTable(labels,labelsh,data2_,caption,TDIR+fname,"kolmDiff3")

#####################
## tabela de diferenciação
# para distribuições uniforme e weibull

#xx=n.linspace(.75,1.25,16,endpoint=True)
xx=n.arange(.70,1.35,0.05)
labels=xx
distsAll=[[g.kolmogorovSmirnovDistance(
        xxx*n.random.random(NA),n.random.random(NA)) for i in range(ND)]
        for xxx in xx]
data=[(n.mean(dd),n.std(dd),n.median(dd),
    ("{:.3f},"*3)[:-1].format(*min3(dd)),
    ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAll]
data_=[]
i=0
for dists in distsAll:
    line=[]
    for calfa in calfas:
        line.append(sum([dist>calfa for dist in dists])/ND)
    data_.append(list(data[i])+line); i+=1
caption=r"""Location and dispersion of $N_c={}$
measurements of $c'$ through simulations
with uniform distributions and $N_o={}$ events each.
$N_b={}$ equal bins were used to make the histograms.
One uniform distribution has the fixed domain $[0,1)$.
The other uniform distribution in each comparison
is also centered around 0.5,
but spread over $b=b_u-b_l$ there $b_l$ and $b_u$ are the lower and upper boudaries.""".format(ND,NA, 30)

labelsh=[r"$b$",r"$\mu(c')$",r"$\sigma(c')$","m(c')","min(c')","max(c')"]
labelsh+=[r"$\overline{{C'({})}}$".format(alfa) for alfa in alfas]
fname="tabUniformDiffSpread.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"kolmDiff3")
i=0
check("diferencas uniformes")

############
## uniformes diferencas pelas medias
xx=n.arange(.0,.65,0.05)
labels=xx+.5
distsAll=[[g.kolmogorovSmirnovDistance(
        n.random.random(NA)+xxx,n.random.random(NA)) for i in range(ND)]
        for xxx in xx]
data=[(n.mean(dd),n.std(dd),n.median(dd),
    ("{:.3f},"*3)[:-1].format(*min3(dd)),
    ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAll]
data_=[]
i=0
for dists in distsAll:
    line=[]
    for calfa in calfas:
        line.append(sum([dist>calfa for dist in dists])/ND)
    data_.append(list(data[i])+line); i+=1
caption=r"""Location and dispersion of $N_c={}$
measurements of $c'$ through simulations
with uniform distributions and $N_o={}$ events each.
$N_b={}$ equal bins were used to make the histograms.
One uniform distribution has the fixed domain $[0,1)$.
The other uniform distribution in each comparison
have varied mean values but always
spread over $b=b_u-b_l$ there $b_l$ and $b_u$ are the lower and upper boudaries.""".format(ND,NA, 30)

labelsh=[r"$\mu$",r"$\mu(c')$",r"$\sigma(c')$","m(c')","min(c')","max(c')"]
labelsh+=[r"$\overline{{C'({})}}$".format(alfa) for alfa in alfas]
fname="tabUniformDiffMean.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"kolmDiff3")
i=0
check("diferencas uniformes pelas médias")



##################
### Diferenças Weibull

xx=n.hstack(([0.01],n.arange(.10,3.,0.2)))
labels=xx
#distsAll=[[g.kolmogorovSmirnovDistance(
#        xxx*n.random.random(NA),n.random.random(NA)) for i in range(ND)]
distsAllW=[[g.kolmogorovSmirnovDistance(
        n.random.weibull(xxx,NA),n.random.weibull(1.5,NA)) for i in range(ND)]

        for xxx in xx]
data=[(n.mean(dd),n.std(dd),n.median(dd),
    ("{:.3f},"*3)[:-1].format(*min3(dd)),
    ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllW]
data_=[]
i=0
for dists in distsAllW:
    line=[]
    for calfa in calfas:
        line.append(sum([dist>calfa for dist in dists])/ND)
    data_.append(list(data[i])+line); i+=1
caption=r"""Location and dispersion of $N_c={}$
measurements of $c'$ through simulations
with 1-parameter Weibull distributions and $N_o={}$ events each.
$N_b={}$ equal bins were used to make the histograms.
One Weibull distribution has the fixed shape parameter $a=1.5$.
The other Weibull distribution in each comparison
has varied values of $a$.""".format(ND,NA, 30)

labelsh=[r"$a$",r"$\mu(c')$",r"$\sigma(c')$","m(c')","min(c')","max(c')"]
labelsh+=[r"$\overline{{C'({})}}$".format(alfa) for alfa in alfas]
fname="tabWeibullDiffShape.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"kolmDiff3")
i=0
check("diferencas Weibull")


############3
## Power law
xx=n.arange(.7,2.7,0.2)
labels=xx
#distsAll=[[g.kolmogorovSmirnovDistance(
#        xxx*n.random.random(NA),n.random.random(NA)) for i in range(ND)]
distsAllW=[[g.kolmogorovSmirnovDistance(
        n.random.power(xxx,NA),n.random.power(1.5,NA)) for i in range(ND)]

        for xxx in xx]
data=[(n.mean(dd),n.std(dd),n.median(dd),
    ("{:.3f},"*3)[:-1].format(*min3(dd)),
    ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllW]
data_=[]
i=0
for dists in distsAllW:
    line=[]
    for calfa in calfas:
        line.append(sum([dist>calfa for dist in dists])/ND)
    data_.append(list(data[i])+line); i+=1
caption=r"""Location and dispersion of $N_c={}$
measurements of $c'$ through simulations
with power function distributions and $N_o={}$ events each.
$N_b={}$ equal bins were used to make the histograms.
One power distribution has the fixed exponent parameter $1-a=2.5$.
The other power function distribution in each comparison
has varied values of $a$.""".format(ND,NA, 30)

labelsh=[r"$a$",r"$\mu(c')$",r"$\sigma(c')$","m(c')","min(c')","max(c')"]
labelsh+=[r"$\overline{{C'({})}}$".format(alfa) for alfa in alfas]
fname="tabPowerDiffShape.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"kolmDiff3")
i=0
check("diferencas Power")





###############3
## aplicações


######
# 
# events in a sample para items of the sample (together known as set of data)
# 
# 

#############
## região crítica?
# hipótese nula?
# distribuições chi-square? lei de potência?
# Kolmogorov-Smirnov distances? https://pypi.python.org/pypi/powerlaw
# discrete cases? http://www.itl.nist.gov/div898/handbook/eda/section3/eda35g.htm
# KS statistics == KS distance?
# bootstrap resampling ... e ... ad hoc
# D statistic, p-value
# the Kolmogorov-Smirnov goodness-of-fit is the D statistic and the KS distance?
# medir Fisher information?

# Another advantage is that it is an exact test (the chi-square goodness-of-fit test depends on an adequate sample size for the approximations to be valid) http://www.itl.nist.gov/div898/handbook/eda/section3/eda35g.htm
# Note that although the K-S test is typically developed in the context of continuous distributions for uncensored and ungrouped data, the test has in fact been extended to discrete distributions and to censored and grouped data.
# We do not discuss those cases here.

# The logarithm transformation may help to overcome cases where the Kolmogorov test data does not seem to fit the assumption that it came from the normal distribution. https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
# If one chooses a critical value of the test statistic Dα such that P(Dn > Dα) = α, then a band of width ±Dα around Fn(x) will entirely contain F(x) with probability 1 − α.


# boas referências: http://stats.stackexchange.com/questions/411/motivation-for-kolmogorov-distance-between-distributions
# Most Monte Carlo studies show that the Anderson-Darling test is more powerful than the Kolmogorov-Smirnov test. It is available in scipy.stats with critical values, and in statsmodels with approximate p-values:

# often not very sensitive in establishing distances between two distributions, and a similar EDF-based test gives a better performance. https://asaip.psu.edu/Articles/beware-the-kolmogorov-smirnov-test
# The Anderson-Darling (AD) test was developed in the 1950s as a weighted CvM test to overcome both of these problems. 
# from scipy.stats import anderson_ksamp
# Bootstrap resampling is conceptually and computationally simple, and the theory underlying the bootstrap guarantee that the resulting significance levels are unbiased for a wide range of situations.

# In R you can also do a bootstrapped KS test sekhon.berkeley.edu/matching/ks.boot.html which gets rid of the continuity requirement – Dr G http://stats.stackexchange.com/questions/13326/can-i-use-kolmogorov-smirnov-to-compare-two-empirical-distributions

# >>> sm.stats.normal_ad(x)
# (0.23016468240712129, 0.80657628536145665)

# https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test
