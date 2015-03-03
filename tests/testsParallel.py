import gmane as g, importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g)
#importlib.reload(g.download)
dreload(g)

loads=g.DownloadGmaneData('/.gmane2/')
loads.downloadListIDS()
#for list_id in loads.list_ids[9:]:
#    loads.downloadListMessages(list_id,end=100000)
# download all files from list with first ID of list_ids

# define uma função que baixa, que já é o loads.download
# manda baixar async umas 30 listas e ve o que rola
pool=mp.Pool(processes=100)

args_=tuple((i,1,1000000,100) for i in loads.list_ids)
#results___=pool.map_async(loads.downloadListMessages,args_)
results__=[pool.apply_async(loads.downloadListMessages,args=x) for x in args_]
