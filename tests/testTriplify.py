import  importlib, os
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
import gmane as g, percolation as P
G=g
importlib.reload(g.listDataStructures)
importlib.reload(g.loadMessages)
importlib.reload(g.triplifyList)
importlib.reload(P.rdf)
importlib.reload(P.utils)
dreload(g,exclude="pytz")

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")
ds=g.ListDataStructures(lm)

dpath='/home/r/.gmane4/'
dl=g.DownloadGmaneData(dpath)
dl.downloadedStats() # might take a while
load_msgs=[]
data_structs=[]
scriptpath=os.path.realpath(__file__)
fpath="./publishing/"
#for list_stat in dl.lists:
#    list_id=list_stat[0]
for list_id in ['gmane.politics.organizations.metareciclagem', 'gmane.comp.gcc.libstdc++.devel', 'gmane.linux.audio.devel', 'gmane.linux.audio.users']:
    load_msgs.append(g.LoadMessages(list_id,basedir=dpath))
    data_structs.append(g.ListDataStructures(load_msgs[-1]))
    foo=G.triplifyList.makeRepo(data_structs[-1],fpath,dpath+list_id,"Linked data of the email list with Gmane id: {}".format(list_id),scriptpath=scriptpath,list_id=list_id)
    mm=data_structs[-1].messages
    ids=data_structs[-1].message_ids
    print("first: ", mm[ids[0]][2], "last:", mm[ids[-1]][2])
 
