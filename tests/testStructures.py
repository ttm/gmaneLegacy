import  importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
import gmane as g
importlib.reload(g.listDataStructures)
importlib.reload(g.loadMessages)
dreload(g,exclude="pytz")

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")
ds=g.ListDataStructures(lm)


dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while
load_msgs=[]
data_structs=[]
for list_stat in dl.lists[:3]:
    list_id=list_stat[0]
    load_msgs.append(g.LoadMessages(list_id,basedir="~/.gmane2/"))
    data_structs.append(g.ListDataStructures(load_msgs[-1]))
    mm=data_structs[-1].messages
    ids=data_structs[-1].message_ids
    print("first: ", mm[ids[0]][2], "last:", mm[ids[-1]][2])
 
