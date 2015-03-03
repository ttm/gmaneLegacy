import gmane as g, importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g)
#importlib.reload(g.download)
dreload(g)

loads=g.DownloadGmaneData('/.gmane2/')
loads.downloadedStats()
# read BASE_DIR/stats.txt
