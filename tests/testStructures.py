import  importlib
import gmane as g
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.messageDataStructures)
dreload(g,exclude="pytz")

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")
ds=g.MessageDataStructures(lm)


