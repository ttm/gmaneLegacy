import gmane as g, importlib
import multiprocessing as mp
from IPython.lib.deepreload import reload as dreload
#importlib.reload(g)
#importlib.reload(g.download)
dreload(g)

dl=g.DownloadGmaneData('/.gmane2/')
dl.downloadedStats()
# read BASE_DIR/stats.txt
