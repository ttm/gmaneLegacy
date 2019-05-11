import gmaneLegacy as g, os
ENV=os.environ["PATH"]
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(g.tableHelpers)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

labels=("l1","label2")
data=[[1,5,7],[3.4,3,7.8]]
tstring=g.makeTables(labels,data)
print(tstring)
row_labels=list(range(10))
sequences=[list(range(30,40)),list(range(50,60))]
partials=[1,2,5]
tstring2=g.parcialSums(row_labels,sequences,partials)

partial_labels=["u.","b.","q."]
datarow_labels=["ELE","LAD"]
tstring3=g.parcialSums(row_labels,sequences,partials,partial_labels,datarow_labels)

dl=g.DownloadGmaneData('~/.gmane2/')
dl.downloadedStats() # might take a while

lm=g.LoadMessages(dl.lists[0][0],basedir="~/.gmane2/")
print("loaded messages")
ds=g.ListDataStructures(lm)
print("made datastructures")
ts=g.TimeStatistics(ds)
print("made overall activity statistics along time")


hi=ts.hours["histogram"]/ts.hours["histogram"].sum()
row_labels=list(range(24))
tstring4=g.parcialSums(row_labels,data=[hi],partials=[1,2,3,4,6,12],partial_labels=["h","2h","3h","4h","6h","12h"],datarow_labels=["LOOB"])

g.writeTex(tstring4,"aqui.tex")
