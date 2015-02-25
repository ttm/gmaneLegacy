import gmane as g, importlib
importlib.reload(g)
importlib.reload(g.download)

loads=g.LoadGmaneData()
loads.downloadListIDS()
for list_id in loads.list_ids:
    loads.downloadListMessages(list_id,end=100000)
# download all files from list with first ID of list_ids
