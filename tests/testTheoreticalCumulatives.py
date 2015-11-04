import numpy as n, pylab as p
from scipy import stats as st
a=st.norm(0,1)
b=st.norm(0.1,1)
domain=n.linspace(-4,4,10000)
avals=a.cdf(domain)
bvals=b.cdf(domain)
diffN=n.abs(avals-bvals).max()

a=st.norm(0,1)
b=st.norm(0,1.2)
domain=n.linspace(-4,4,10000)
avals=a.cdf(domain)
bvals=b.cdf(domain)
diffN2=n.abs(avals-bvals).max()

a=st.uniform(0,1)
b=st.uniform(0.05,1.05)
domain=n.linspace(0,1.05,10000)
avals=a.cdf(domain)
bvals=b.cdf(domain)
diffU=n.abs(avals-bvals).max()

a=st.uniform(0,1)
b=st.uniform(-0.05,1.05)
domain=n.linspace(0,1.05,10000)
avals=a.cdf(domain)
bvals=b.cdf(domain)
diffU2=n.abs(avals-bvals).max()

#a=st.weibull(1.5)
#b=st.weibull(1.7)
#domain=n.linspace(0,1.05,10000)
#avals=a.cdf(domain)
#bvals=b.cdf(domain)
#diffW=n.abs(avals-bvals).max()

#a=st.power(1.5)
#b=st.power(1.7)
#domain=n.linspace(0,1.05,10000)
#avals=a.cdf(domain)
#bvals=b.cdf(domain)
#diffP=n.abs(avals-bvals).max()

#x = n.arange(1,100.)/50.
x=n.linspace(0,20,100000)
step=x[1]-x[0]
def weib(x,nn,a):
    return (a / nn) * (x / nn)**(a - 1) * n.exp(-(x / nn)**a)

#count, bins, ignored = p.hist(n.random.weibull(5.,1000))
#x = n.arange(1,100.)/50.
#scale = count.max()/weib(x, 1., 5.).max()
W=weib(x, 1., 1.5)
W_=W/(W*step).sum()
W2=weib(x, 1., 1.7)
W2_=W2/(W2*step).sum()
diffW=n.abs(W_-W2_).max()
#p.plot(x, W_)
#p.plot(x, W2_)
##p.plot(x, weib(x, 1., 5.)*scale)
#p.show()

a=st.powerlaw(1.5)
b=st.powerlaw(1.7)
domain=n.linspace(0,5.05,10000)
avals=a.cdf(domain)
bvals=b.cdf(domain)
diffP=n.abs(avals-bvals).max()

print("distancias de KS para os modelos matematicos:", diffN,diffN2,diffU,diffU2,diffW,diffP)
# distancias de KS para os modelos matematicos:
# 0.0398776116762 0.0439947104098 0.0952338090952 0.047619047619 0.128565475845 0.0460149130584





