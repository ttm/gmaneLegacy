import gmane as g, os
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

