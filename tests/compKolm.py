import gmaneLegacy as g, numpy as n
from scipy.stats import ks_2samp

a=n.random.random(1000)
b=n.random.random(1000)
b_=b+.3

aa=g.kolmogorovSmirnovDistance(a,b)
bb=ks_2samp(a,b)

aa_=g.kolmogorovSmirnovDistance(a,b_)
bb_=ks_2samp(a,b_)
b__=b+.07
aa2=g.kolmogorovSmirnovDistance(a,b__)
bb2=ks_2samp(a,b__)

