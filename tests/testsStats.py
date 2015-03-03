import gmane as g, importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g)
#importlib.reload(g.download)
dreload(g)

loads2=g.DownloadGmaneData('/.gmane2/')
loads2.downloadedStats()
# read BASE_DIR/stats.txt
