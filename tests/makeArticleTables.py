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
PDIR="pickledir/"
dss=[]
tss=[]
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
for lid in dl.downloaded_lists:
    print(lid)
    label=labels[lid]
    lm=g.LoadMessages(lid,basedir="~/.gmane4/")
    print(label+"{0:.2f} for loading messages".format(T.time()-TT)); TT=T.time()
    ds=g.ListDataStructures(lm,text="no")
    print(label+"{0:.2f} for data structures".format(T.time()-TT)); TT=T.time()
    pDump(ds,"{}ds{}.pickle".format(PDIR,label))
    ts=g.TimeStatistics(ds)
    print(label+"{0:.2f} for statistics along time".format(T.time()-TT)); TT=T.time()
    pDump(ds,"{}ts{}.pickle".format(PDIR,label))
    dss.append(ds)
    tss.append(ts)
#f=open("4listas_.pickle","wb")
#pickle.dump([dl,dss,tss],f,-1)
#f.close()
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject
for lid in dl.downloaded_lists:
    label=labels[lid]
    dss.append(pRead("{}ds{}.pickle".format(PDIR,label)))
    print(label+"{0:.2f} for PICKLE loading data structures".format(T.time()-TT)); TT=T.time()
    tss.append(pRead("{}ts{}.pickle".format(PDIR,label)))
    print(label+"{0:.2f} for PICKLE loading time statistics".format(T.time()-TT)); TT=T.time()


#f=open("4listas_.pickle","rb")
#dl,dss,tss=pickle.load(f)
#f.close()

order=[2,1,3,0] # LAU LAD MET CPP
labels_=[]
data_=[]
#for i in order[:1]:
for i in [0]:
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

labels_=["seconds","minutes","hours","weekdays","monthdays","months"]
data_=[]

# medidas: circular mean, circular std, circular variance, circular dispersion, max/min
#for i in order[:1]:
for i in [0]:
    ts=tss[i]
    data_=[]
    data_.append([
                  #ts.seconds["circular_measures"]["circular_mean"],
                  "--//--",
                  ts.seconds["circular_measures"]["std_unity_radius"],
                  ts.seconds["circular_measures"]["variance_unity_radius"],
                  ts.seconds["circular_measures"]["circular_dispersion"],
                  ts.seconds["max_discrepancy"],
        ])
    data_.append([
                  #ts.minutes["circular_measures"]["circular_mean"],
                  "--//--",
                  ts.minutes["circular_measures"]["std_unity_radius"],
                  ts.minutes["circular_measures"]["variance_unity_radius"],
                  ts.minutes["circular_measures"]["circular_dispersion"],
                  ts.minutes["max_discrepancy"],
        ])
    data_.append([ts.hours["circular_measures"]["circular_mean"],
            ts.hours["circular_measures"]["std_unity_radius"],
            ts.hours["circular_measures"]["variance_unity_radius"],
            ts.hours["circular_measures"]["circular_dispersion"],
            ts.hours["max_discrepancy"],
        ])
    data_.append([ts.weekdays["circular_measures"]["circular_mean"],
                  ts.weekdays["circular_measures"]["std_unity_radius"],
                  ts.weekdays["circular_measures"]["variance_unity_radius"],
                  ts.weekdays["circular_measures"]["circular_dispersion"],
                  ts.weekdays["max_discrepancy"],
        ])
    data_.append([
                  #ts.monthdays["circular_measures"]["circular_mean"],
                  "--//--",
                  ts.monthdays["circular_measures"]["std_unity_radius"],
                  ts.monthdays["circular_measures"]["variance_unity_radius"],
                  ts.monthdays["circular_measures"]["circular_dispersion"],
                  ts.monthdays["max_discrepancy"],
        ])
    data_.append([ts.months["circular_measures"]["circular_mean"],
                  ts.months["circular_measures"]["std_unity_radius"],
                  ts.months["circular_measures"]["variance_unity_radius"],
                  ts.months["circular_measures"]["circular_dispersion"],
                  ts.months["max_discrepancy"],
        ])
    tstring=g.makeTables(labels_,data_,True)
    label=labels[dl.downloaded_lists[i]]
    g.writeTex(tstring,TDIR+"tab2Time{}.tex".format(label))
print(label+"{0:.2f} for making time statistics table".format(T.time()-TT)); TT=T.time()
