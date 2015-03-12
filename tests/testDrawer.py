#import multiprocessing as mp
#import  importlib
#from IPython.lib.deepreload import reload as dreload
import os
import gmane as g
#importlib.reload(g.loadMessages)
#importlib.reload(g.listDataStructures)
#importlib.reload(g.interactionNetwork)
#importlib.reload(g.networkMeasures)
#importlib.reload(g.networkPartitioning)
#importlib.reload(g.networkDrawer)
#dreload(g,exclude="pytz")

dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while
print("made liststats")

lm=g.LoadMessages(dl.lists[0][0],basedir="~/.gmane2/")
print("loaded messages")
ds=g.ListDataStructures(lm)
print("made datastructures")
iN=g.InteractionNetwork(ds)
print("made interaction network")
nm=g.NetworkMeasures(iN)
print("network mesaures")
np=g.NetworkPartitioning(nm,3)
print("partitioned network")


nd=g.NetworkDrawer()
print("drawer started")
nd.makeLayout(nm)
print("gave (x,y) for each author with 5-15-80")
nd2=g.NetworkDrawer()
print("drawer two started")
nd2.makeLayout(nm,np)
print("gave (x,y) for each author with \
sectors by comparison with Erdos-Renyi")

nd.drawNetwork( iN,nm ,"test.png")
nd2.drawNetwork( iN,nm,"test2.png")

N=100
dN=1
print("please wait while all images are finished")
for i in range(50):
    ds=g.ListDataStructures(lm.messages[i:i+N])
    iN=g.InteractionNetwork(ds)
    nm=g.NetworkMeasures(iN)

    nd.drawNetwork( iN,nm ,"seq3/im{:09}.png".format(i))
    nd2.drawNetwork( iN,nm,"seq4/im{:09}.png".format(i))
print("please wait while images become movies")
os.system("avconv -f image2 -i seq3/im%09d.png -vcodec mpeg4 -y movie5-15-80.mp4")
os.system("avconv -f image2 -i seq4/im%09d.png -vcodec mpeg4 -y movieErdosSectorialiation.mp4")







