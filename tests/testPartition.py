import multiprocessing as mp
import  importlib
from IPython.lib.deepreload import reload as dreload
import gmane as g
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.interactionNetwork)
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

