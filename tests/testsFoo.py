import gmaneLegacy as g, importlib
importlib.reload(g)
importlib.reload(g.download)

loads=g.LoadGmaneData()
loads.downloadListIDS()
for list_id in loads.list_ids[9:]:
    loads.downloadListMessages(list_id,end=100000)
# download all files from list with first ID of list_ids

# define uma função que baixa, que já é o loads.download
# manda baixar async umas 30 listas e ve o que rola
