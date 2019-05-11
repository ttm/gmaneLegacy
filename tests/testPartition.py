import multiprocessing as mp
import  importlib
from IPython.lib.deepreload import reload as dreload
import gmaneLegacy as g
#importlib.reload(g.loadMessages)
#importlib.reload(g.listDataStructures)
#importlib.reload(g.interactionNetwork)
importlib.reload(g.networkMeasures)
importlib.reload(g.networkPartitioning)
dreload(g,exclude="pytz")

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

np=g.NetworkPartitioning(nm)
print("partitioned network")
np2=g.NetworkPartitioning(nm,2)
print("partitioned network")
np3=g.NetworkPartitioning(nm,3)
print("partitioned network")


np_=g.NetworkPartitioning(nm, 1,"g")
print("partitioned network")
np2_=g.NetworkPartitioning(nm,2,"g")
print("partitioned network")
np3_=g.NetworkPartitioning(nm,3,"g")
print("partitioned network")

ps=[np,np2,np3] # partition by strength
pg=[np_,np2_,np3_] # partition by degree

def N(pp):
    ll=[(len(i[0]),len(i[1]),len(i[2])) for 
            i in [pp.sectorialized_agents__]][0]
    return ll
for p1, p2 in zip(ps,pg):
    print("{}, {}".format(N(p1),N(p2)))

