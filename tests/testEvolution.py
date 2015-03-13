import gmane as g, os
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.networkDrawer)
importlib.reload(g.networkEvolution)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while
print("made liststats")

lm=g.LoadMessages(dl.lists[0][0],basedir="~/.gmane2/")
print("loaded messages")

#ne=g.NetworkEvolution(step_size=20)
#ne.evolveRaw(lm.messages[:500])
#ne.makeVideo(framerate=12)

ne=g.NetworkEvolution(step_size=10)
ne.evolveRaw(lm.messages,imagerate=4,erdos_sectors=True)
ne.makeVideo()
