import gmane as g, numpy as n, os, pylab as p
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.networkMeasures)
importlib.reload(g.pca)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

individuals=n.array([[1,1],[-1,1]])

vals=n.random.random(200)*100
# create x, y on first, second and fourth quadrants bisectors 
x1=vals
y1=vals
x2=-vals
y2=vals
x3=vals
y3=-vals

xx=n.hstack((x1,x2,x3))
yy=n.hstack((y1,y2,y3))

M=n.vstack((xx,yy)) 
# M[0] has all measures for the same metric
# i.e. len(M[0]) is number of observations
# and M[i] returns all measurements on metric i

pca=g.PCA(M)
pca.plot()

###  Make network PCA with partitions ###
dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while
print("made liststats")

lm=g.LoadMessages(dl.lists[0][0],basedir="~/.gmane2/")
print("loaded messages")
ds=g.ListDataStructures(lm)
print("made datastructures")
iN=g.InteractionNetwork(ds)
print("made interaction network")
nm=g.NetworkMeasures(iN)
print("network mesaures")

# Make PCA of degree, betweenness and clustering
# with in, out and total degree and strengths
# and with symmetry related measures
npca=g.NetworkPCA(nm)

# Make network partitioning
np=g.NetworkPartitioning(nm,3,"g")
print("partitioned network")

# Plot PCA with partitions
npca=g.NetworkPCA(nm,np)
