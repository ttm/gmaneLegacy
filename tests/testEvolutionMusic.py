import gmane as g, mass as m, os
ENV=os.environ["PATH"]
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(g.evolutionMusic)
importlib.reload(m.pieces.fourHubsDance)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV
#dreload(m)
#os.environ["PATH"]=ENV

#dl=g.DownloadGmaneData('/disco/.gmane2/')
#dl.downloadedStats() # might take a while
#print("made liststats")

lm=g.LoadMessages("gmane.linux.audio.users",4000,basedir="/disco/.gmane/")
#lm=g.LoadMessages("gmane.linux.audio.users",800,basedir="/disco/.gmane/")
print("loaded messages")
#
##ne=g.NetworkEvolution(step_size=20)
##ne.evolveRaw(lm.messages[:500])
##ne.makeVideo(framerate=12)
#
ne=g.NetworkEvolution(window_size=400, step_size=40)
print("evolution started")
ne.evolveRaw(lm.messages,imagerate=4,erdos_sectors=True)
print("network evolved")

em=g.EvolutionMusic()
print("music is done")
