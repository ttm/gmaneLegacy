import multiprocessing as mp
import  importlib
from IPython.lib.deepreload import reload as dreload
import gmane as g
importlib.reload(g.listDataStructures)
importlib.reload(g.loadMessages)
importlib.reload(g.interactionNetwork)
importlib.reload(g.networkMeasures)
dreload(g,exclude="pytz")

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")
ds=g.ListDataStructures(lm)
iN=g.InteractionNetwork(ds)
nm=g.NetworkMeasures(iN)

