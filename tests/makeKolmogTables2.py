import gmane as g, os, pickle, time, numpy as n, nltk as k, sys
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g.pca)
#importlib.reload(g.loadMessages)
#importlib.reload(g.listDataStructures)
#importlib.reload(g.textUtils)
#importlib.reload(g.tableHelpers)
importlib.reload(g.ksStatistics)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
TDIR2="/home/r/repos/kolmogorov-smirnov/aux/"
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
#NA=10**3 # numero de amostras
#ND=NC=10**2 # numero de comparações de distribuições
ks=g.KSReferences()
#ks.makeAllTables() # simulations
#ks.makeKSAnalysis() # empirical


