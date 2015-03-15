import gmane as g, os
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g.listDataStructures)
#importlib.reload(g.loadMessages)
importlib.reload(g.interactionNetwork)
importlib.reload(g.networkMeasures)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")
ds=g.ListDataStructures(lm)
iN=g.InteractionNetwork(ds)
nm=g.NetworkMeasures(iN)


dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while

lm=g.LoadMessages(dl.lists[0][0],basedir="~/.gmane2/")
print("loaded messages")
ds=g.ListDataStructures(lm)
print("made datastructures")
iN=g.InteractionNetwork(ds)
print("made interaction network")
nm=g.NetworkMeasures(iN)
print("network mesaures")


