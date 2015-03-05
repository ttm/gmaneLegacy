import gmane as g, importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g)
#importlib.reload(g.download)
dreload(g)

lm=g.LoadMessages("gmane.ietf.rfc822",10,basedir="~/.gmane2/")

dl=g.DownloadGmaneData('~/.gmane2/')
dl.getDownloadedLists()
lms=[]
for list_id in dl.downloaded_lists[:10]:
    print(list_id)
    lms.append(g.LoadMessages(list_id,basedir="~/.gmane2/"))

# to download first three lists with the greated number
# of downloaded messages, do:
dl.downloadedStats() # might take a while
lms2=[]
for list_stat in dl.lists[:3]:
    list_id=list_stat[0]
    lms2.append(g.LoadMessages(list_id,basedir="~/.gmane2/"))
    

