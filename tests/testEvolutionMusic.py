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

em=g.EvolutionMusic()
