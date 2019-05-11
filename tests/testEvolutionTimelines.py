import gmaneLegacy as g, os
ENV=os.environ["PATH"]
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(g.evolutionTimelines)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

et=g.EvolutionTimelines()




