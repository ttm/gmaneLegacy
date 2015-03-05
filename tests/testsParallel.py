import gmane as g, importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g)
#importlib.reload(g.download)
dreload(g)

dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadListIDS()
#for list_id in loads.list_ids[9:]:
#    loads.downloadListMessages(list_id,end=100000)
# download all files from list with first ID of list_ids

# define uma função que baixa, que já é o loads.download
# manda baixar async umas 30 listas e ve o que rola
pool=mp.Pool(processes=100)

args_=tuple((i,1,1000000,100) for i in dl.list_ids[:200])
#results___=pool.map_async(loads.downloadListMessages,args_)
results__=[pool.apply_async(dl.downloadListMessages,args=x) for x in args_]
