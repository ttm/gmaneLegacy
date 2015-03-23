import gmane as g, os
ENV=os.environ["PATH"]
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(g.evolutionMusic)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

em=g.EvolutionMusic()
