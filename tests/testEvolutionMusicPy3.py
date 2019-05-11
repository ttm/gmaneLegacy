# import gmane as g, os, music as m
# ENV=os.environ["PATH"]
# import  importlib
# #from IPython.lib.deepreload import reload as dreload
# importlib.reload(g.evolutionMusic)
# importlib.reload(m.pieces.fourHubsDance)
# #dreload(g,exclude="pytz")
# os.environ["PATH"]=ENV
#dreload(m)
#os.environ["PATH"]=ENV
import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if ("gmane" in key):
        del sys.modules[key]
    if ("musicLegagy" in key):
        try:
            del sys.modules[key]
        except:
            pass
import gmaneLegacy as g, os, musicLegacy as m

#dl=g.DownloadGmaneData('/disco/.gmane2/')
#dl.downloadedStats() # might take a while
#print("made liststats")

lm=g.LoadMessages("cpp",4000,basedir="~/repos/versinus/data/gmaneMessages/mbox/")
#lm=g.LoadMessages("gmane.linux.audio.users",800,basedir="/disco/.gmane/")
print("loaded messages")
#
##ne=g.NetworkEvolution(step_size=20)
##ne.evolveRaw(lm.messages[:500])
##ne.makeVideo(framerate=12)
#
ne=g.NetworkEvolution(window_size=40, step_size=40)
print("evolution started")
ne.evolveRaw(lm.messages,imagerate=4,erdos_sectors=True)
print("network evolved")

em=g.EvolutionMusic()
print("music is done")
