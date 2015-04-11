import gmane as g, os, pickle, time as T
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.timeStatistics)
importlib.reload(g.tableHelpers)
#importlib.reload(g.interactionNetwork)
#importlib.reload(g.networkMeasures)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

labels={'gmane.comp.gcc.libstdc++.devel':"CPP", 'gmane.linux.audio.devel':"LAD", 'gmane.linux.audio.users':"LAU", 'gmane.politics.organizations.metareciclagem':"MET"}
print("initializing")
dl=g.DownloadGmaneData('~/.gmane4/')
TT=T.time()
print("{0:.2f} for initializing download dir initializing".format(T.time()-TT)); TT=T.time()
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject

#### DATA STRUCTURES
#for lid in dl.downloaded_lists:
#    print(lid)
#    label=labels[lid]
#    lm=g.LoadMessages(lid,basedir="~/.gmane4/")
#    print(label+"{0:.2f} for loading messages".format(T.time()-TT)); TT=T.time()
#    ds=g.ListDataStructures(lm,text="no")
#    print(label+"{0:.2f} for data structures".format(T.time()-TT)); TT=T.time()
#    pDump(ds,"{}ds{}.pickle".format(PDIR,label))
#    dss.append(ds)

PDIR="pickledir/"
dss=[]
for lid in dl.downloaded_lists:
    label=labels[lid]
    dss.append(pRead("{}ds{}.pickle".format(PDIR,label)))
    print(label+"{0:.2f} for PICKLE loading data structures".format(T.time()-TT)); TT=T.time()

##### TIME STATISTICS
tss=[]; count=0
for lid in dl.downloaded_lists:
    label=labels[lid]
    ds=dss[count]; count+=1
    ts=g.TimeStatistics(ds)
    print(label+"{0:.2f} for statistics along time".format(T.time()-TT)); TT=T.time()
    pDump(ts,"{}ts{}.pickle".format(PDIR,label))
    tss.append(ts)
for lid in dl.downloaded_lists:
    label=labels[lid]
    tss.append(pRead("{}ts{}.pickle".format(PDIR,label)))
    print(label+"{0:.2f} for PICKLE loading time statistics".format(T.time()-TT)); TT=T.time()

##pDump([dl,dss,tss],"4listas_.pickle")
#f=open("4listas_.pickle","rb")
#dl,dss,tss=pickle.load(f)
#f.close()

order=[2,1,3,0] # LAU LAD MET CPP
labels_=[]
data_=[]
for i in order[:1]:
#for i in [0]:
    labels_.append(labels[dl.downloaded_lists[i]])
    ds=dss[i]
    date1=ds.messages[ds.message_ids[0]][2].isoformat().split("T")[0]
    date2=ds.messages[ds.message_ids[-1]][2].isoformat().split("T")[0]
    N=ds.n_authors
    Gamma=len([i for i in ds.message_ids if ds.messages[i][1]==None])
    M_=20000-ds.n_messages
    data_.append([date1,date2,N,Gamma,M_])
tstring=g.makeTables(labels_,data_)
print(tstring)
TDIR="tables/"
FDIR="figs/"
print(label+"{0:.2f} for making overall table".format(T.time()-TT)); TT=T.time()


g.writeTex(tstring,TDIR+"tab1Geral.tex")

data_=[]
# medidas: circular mean, circular std, circular variance, circular dispersion, max/min
def circMeasures(tdict,mean=True):
    if mean:
       return [tdict["circular_measures"]["circular_mean"],
            tdict["circular_measures"]["std_unity_radius"],
            tdict["circular_measures"]["variance_unity_radius"],
            tdict["circular_measures"]["circular_dispersion"],
            tdict["max_discrepancy"],
        ]
    else:
       return ["--//--",
            tdict["circular_measures"]["std_unity_radius"],
            tdict["circular_measures"]["variance_unity_radius"],
            tdict["circular_measures"]["circular_dispersion"],
            tdict["max_discrepancy"],
        ]
labels_=["seconds","minutes","hours","weekdays","month days","months"]
for i in order:
    ts=tss[i]
    data_=[]
    data_.append(circMeasures(ts.seconds,False))
    data_.append(circMeasures(ts.minutes,False))
    data_.append(circMeasures(ts.hours))
    data_.append(circMeasures(ts.weekdays))
    data_.append(circMeasures(ts.monthdays,False))
    data_.append(circMeasures(ts.months))
    tstring=g.makeTables(labels_,data_,True)
    label=labels[dl.downloaded_lists[i]]
    g.writeTex(tstring,TDIR+"tab2Time{}.tex".format(label))
print(label+"{0:.2f} for making time statistics table".format(T.time()-TT)); TT=T.time()

# Make at least time table inline for
# hours of the day,
row_labels=["{}h".format(i) for i in range(24)]
for i in order:
    ts=tss[i]
    hi=100*ts.hours["histogram"]/ts.hours["histogram"].sum()
    tstring=g.parcialSums(row_labels,data=[hi],partials=[1,2,3,4,6,12],partial_labels=["1h","2h","3h","4h","6h","12h"])
    label=labels[dl.downloaded_lists[i]]
    g.writeTex(tstring,TDIR+"tabHours{}.tex".format(label))

his=[100*tss[i].hours["histogram"]/tss[i].hours["histogram"].sum() for i in order]
datarow_labels=["LAU","LAD","MET","CPP"]
tstring=g.parcialSums(row_labels,data=his,partials=[1,4,6,12],partial_labels=["1h","4h","6h","12h"], datarow_labels=datarow_labels)
g.writeTex(tstring,TDIR+"tabHoursALL.tex".format(label))

# days of the week
data_=[100*tss[i].weekdays["histogram"]/tss[i].weekdays["histogram"].sum() for i in order]
labels_=["LAU","LAD","MET","CPP"]
tstring=g.makeTables(labels_,data_,True)
g.writeTex(tstring,TDIR+"tabWeekdays.tex")

# days of the month and
row_labels=["{}".format(i+1) for i in range(30)]
for i in order:
    ts=tss[i]
    hi=100*ts.monthdays["histogram"]/ts.monthdays["histogram"].sum()
    tstring=g.parcialSums(row_labels,data=[hi],partials=[1,5,10,15],partial_labels=["1 day","5","10","15 days"])
    label=labels[dl.downloaded_lists[i]]
    g.writeTex(tstring,TDIR+"tabMonthdays{}.tex".format(label))

his=[100*tss[i].monthdays["histogram"]/tss[i].monthdays["histogram"].sum() for i in order]
datarow_labels=["LAU","LAD","MET","CPP"]
tstring=g.parcialSums(row_labels,data=his,partials=[1,5,10,15],partial_labels=["1 day","5 days","15 days"], datarow_labels=datarow_labels)
g.writeTex(tstring,TDIR+"tabMonthdaysALL.tex")

# months of the year
row_labels=["Jan","Fev","Mar","Apr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
for i in order:
    ts=tss[i]
    hi=100*ts.months["histogram"]/ts.months["histogram"].sum()
    tstring=g.parcialSums(row_labels,data=[hi],partials=[1,2,3,4,6],partial_labels=["m.","b.","t.","q.","s."])
    label=labels[dl.downloaded_lists[i]]
    g.writeTex(tstring,TDIR+"tabMonths{}.tex".format(label))

his=[100*tss[i].months["histogram"]/tss[i].months["histogram"].sum() for i in order]
datarow_labels=["LAU","LAD","MET","CPP"]
tstring=g.parcialSums(row_labels,data=his,partials=[1,2,3,4,6],partial_labels=["m.","b.","t.","q.","s."], datarow_labels=datarow_labels)
g.writeTex(tstring,TDIR+"tabMonthsALL.tex")






