import  importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
import gmane as g
importlib.reload(g.listDataStructures)
importlib.reload(g.loadMessages)
importlib.reload(g.interactionNetwork)
dreload(g,exclude="pytz")

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")
ds=g.ListDataStructures(lm)
iN=g.InteractionNetwork(ds)

dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while
load_msgs=[]
data_structs=[]
networks=[]
for list_stat in dl.lists[:10]:
    list_id=list_stat[0]
    load_msgs.append(g.LoadMessages(list_id,basedir="~/.gmane2/"))
    data_structs.append(g.ListDataStructures(load_msgs[-1]))
    networks.append(g.InteractionNetwork(data_structs[-1]))
    print("number of nodes: {}, number of edges: {}, number of messages: {} or {} or {}/{}, number of empty messages: {}".format(
            networks[-1].g.number_of_nodes(),
            networks[-1].g.number_of_edges(),
            data_structs[-1].n_messages,
            load_msgs[-1].n_messages,
            list_stat[1]["count_msgs"],list_stat[1]["count_empty"],
            len(data_structs[-1].empty_ids)))
 
