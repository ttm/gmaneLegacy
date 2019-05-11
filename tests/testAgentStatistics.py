import gmaneLegacy as g, os
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.agentStatistics)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while

lm=g.LoadMessages(dl.lists[0][0],basedir="~/.gmane2/")
print("loaded messages")
ds=g.ListDataStructures(lm)
print("made datastructures")
ps=g.AgentStatistics(ds)
print("made overall activity statistics among agents")



