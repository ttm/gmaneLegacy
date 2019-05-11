import gmaneLegacy as g, os, pickle, time as T, numpy as n
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(g.pca)
importlib.reload(g.loadMessages)
importlib.reload(g.listDataStructures)
importlib.reload(g.timeStatistics)
importlib.reload(g.agentStatistics)
importlib.reload(g.tableHelpers)
importlib.reload(g.networkEvolution)
importlib.reload(g.evolutionTimelines)
#importlib.reload(g.interactionNetwork)
#importlib.reload(g.networkMeasures)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

labels={'gmane.comp.gcc.libstdc++.devel':"CPP", 'gmane.linux.audio.devel':"LAD", 'gmane.linux.audio.users':"LAU", 'gmane.politics.organizations.metareciclagem':"MET"}
##print("initializing")
dl=g.DownloadGmaneData('~/.gmane4/')
TT=T.time()
##print("{0:.2f} for initializing download dir initializing".format(T.time()-TT)); TT=T.time()
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject
##
###### DATA STRUCTURES
dss=[]
PDIR="pickledir/"
###for lid in dl.downloaded_lists:
###    print(lid)
###    label=labels[lid]
###    lm=g.LoadMessages(lid,basedir="~/.gmane4/")
###    print(label+"{0:.2f} for loading messages".format(T.time()-TT)); TT=T.time()
###    ds=g.ListDataStructures(lm,text="no")
###    print(label+"{0:.2f} for data structures".format(T.time()-TT)); TT=T.time()
###    pDump(ds,"{}ds{}.pickle".format(PDIR,label))
###    dss.append(ds)
##
for lid in dl.downloaded_lists:
    label=labels[lid]
    dss.append(pRead("{}ds{}.pickle".format(PDIR,label)))
    print(label+"{0:.2f} for PICKLE loading data structures".format(T.time()-TT)); TT=T.time()
##
######## TIME STATISTICS
tss=[]; count=0
for lid in dl.downloaded_lists:
    label=labels[lid]
    ds=dss[count]; count+=1
    ts=g.TimeStatistics(ds)
    print(label+"{0:.2f} for statistics along time".format(T.time()-TT)); TT=T.time()
    pDump(ts,"{}ts{}.pickle".format(PDIR,label))
    tss.append(ts)
#for lid in dl.downloaded_lists:
#    label=labels[lid]
#    tss.append(pRead("{}ts{}.pickle".format(PDIR,label)))
#    print(label+"{0:.2f} for PICKLE loading time statistics".format(T.time()-TT)); TT=T.time()
##
####pDump([dl,dss,tss],"4listas_.pickle")
###f=open("4listas_.pickle","rb") # DEPRECATED
###dl,dss,tss=pickle.load(f) # DEPRECATED
###f.close()
##
order=[2,1,3,0] # LAU LAD MET CPP
#labels_=[]
#data_=[]
##for i in order:
###for i in [0]:
##    labels_.append(labels[dl.downloaded_lists[i]])
##    ds=dss[i]
##    date1=ds.messages[ds.message_ids[0]][2].isoformat().split("T")[0]
##    date2=ds.messages[ds.message_ids[-1]][2].isoformat().split("T")[0]
##    N=ds.n_authors
##    Gamma=len([i for i in ds.message_ids if ds.messages[i][1]==None])
##    M_=20000-ds.n_messages
##    data_.append([date1,date2,N,Gamma,M_])
##tstring=g.makeTables(labels_,data_)
##print(tstring)
##TDIR="tables/"
TDIR="/home/r/repos/stabilityInteraction/tables/"
#FDIR="figs/"
#print(label+"{0:.2f} for making overall table".format(T.time()-TT)); TT=T.time()
#
##g.writeTex(tstring,TDIR+"tab1Geral.tex")
#
#data_=[]
### medidas: circular mean, circular std, circular variance, circular dispersion, max/min
#def circMeasures(tdict,mean=True):
#    if mean:
#       return [tdict["circular_measures"]["circular_mean"],
#            tdict["circular_measures"]["std_unity_radius"],
#            tdict["circular_measures"]["variance_unity_radius"],
#            tdict["circular_measures"]["circular_dispersion"],
#            tdict["max_discrepancy"],
#            tdict["max_discrepancy_"][0],
#            tdict["max_discrepancy_"][1],
#        ]
#    else:
#       return ["--//--",
#            tdict["circular_measures"]["std_unity_radius"],
#            tdict["circular_measures"]["variance_unity_radius"],
#            tdict["circular_measures"]["circular_dispersion"],
#            tdict["max_discrepancy"],
#            tdict["max_discrepancy_"][0],
#            tdict["max_discrepancy_"][1],
#        ]
#labels_=["seconds","minutes","hours","weekdays","month days","months"]
#for i in order:
#    ts=tss[i]
#    data_=[]
#    data_.append(circMeasures(ts.seconds,False))
#    data_.append(circMeasures(ts.minutes,False))
#    data_.append(circMeasures(ts.hours))
#    data_.append(circMeasures(ts.weekdays))
#    data_.append(circMeasures(ts.monthdays))
#    data_.append(circMeasures(ts.months))
#    tstring=g.makeTables(labels_,data_,True)
#    label=labels[dl.downloaded_lists[i]]
#    g.writeTex(tstring,TDIR+"tab2Time{}.tex".format(label))
#print(label+"{0:.2f} for making time statistics table".format(T.time()-TT)); TT=T.time()
#sys.exit()
##
### Make at least time table inline for
### hours of the day,
#row_labels=["{}h".format(i) for i in range(24)]
#for i in order:
#    ts=tss[i]
#    hi=100*ts.hours["histogram"]/ts.hours["histogram"].sum()
#    tstring=g.partialSums(row_labels,data=[hi],partials=[1,2,3,4,6,12],partial_labels=["1h","2h","3h","4h","6h","12h"])
#    label=labels[dl.downloaded_lists[i]]
#    g.writeTex(tstring,TDIR+"tabHours{}.tex".format(label))
#lines=g.markEntries(TDIR+"tabHours{}.tex".format(label),"textbf")
##
##his=[100*tss[i].hours["histogram"]/tss[i].hours["histogram"].sum() for i in order]
##datarow_labels=["LAU","LAD","MET","CPP"]
##tstring=g.partialSums(row_labels,data=his,partials=[1,4,6,12],partial_labels=["1h","4h","6h","12h"], datarow_labels=datarow_labels)
##g.writeTex(tstring,TDIR+"tabHoursALL.tex".format(label))
##
### days of the week
##data_=[100*tss[i].weekdays["histogram"]/tss[i].weekdays["histogram"].sum() for i in order]
##labels_=["LAU","LAD","MET","CPP"]
##tstring=g.makeTables(labels_,data_,True)
##g.writeTex(tstring,TDIR+"tabWeekdays.tex")
##
## days of the month and
#row_labels=["{}".format(i+1) for i in range(30)]
#for i in order:
#    ts=tss[i]
#    hi=100*ts.monthdays["histogram"]/ts.monthdays["histogram"].sum()
#    tstring=g.partialSums(row_labels,data=[hi],partials=[1,5,10,15],partial_labels=["1 day","5","10","15 days"])
#    label=labels[dl.downloaded_lists[i]]
#    g.writeTex(tstring,TDIR+"tabMonthdays{}.tex".format(label))
#
#his=[100*tss[i].monthdays["histogram"]/tss[i].monthdays["histogram"].sum() for i in order]
#datarow_labels=["LAU","LAD","MET","CPP"]
#tstring=g.partialSums(row_labels,data=his,partials=[1,5,10,15],partial_labels=["1 day","5 days","10 days","15 days"], datarow_labels=datarow_labels)
#g.writeTex(tstring,TDIR+"tabMonthdaysALL.tex")

## months of the year
#row_labels=["Jan","Fev","Mar","Apr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
#for i in order:
#    ts=tss[i]
#    hi=100*ts.months["histogram"]/ts.months["histogram"].sum()
#    tstring=g.partialSums(row_labels,data=[hi],partials=[1,2,3,4,6],partial_labels=["m.","b.","t.","q.","s."])
#    label=labels[dl.downloaded_lists[i]]
#    g.writeTex(tstring,TDIR+"tabMonths{}.tex".format(label))
#
#his=[100*tss[i].months["histogram"]/tss[i].months["histogram"].sum() for i in order]
#datarow_labels=["LAU","LAD","MET","CPP"]
#tstring=g.partialSums(row_labels,data=his,partials=[1,2,3,4,6],partial_labels=["m.","b.","t.","q.","s."], datarow_labels=datarow_labels)
#g.writeTex(tstring,TDIR+"tabMonthsALL.tex")
##
NEs=[] # for evolutions of the networks
##for i, lid in enumerate(dl.downloaded_lists):
##    label=labels[lid]
##    ds=dss[i]
##    NEs.append(
##            g.NetworkEvolution(window_size=1000,step_size=1000,tdir="evoPCA{}".format(label)))
##    NEs[-1].evolveDataStructures(ds)
##    pDump(NEs[-1],"{}neP{}.pickle".format(PDIR,label))
##    print(label+"{0:.2f} for evolving and PICKLE pickle dumping PCA structures".format(T.time()-TT)); TT=T.time()
#for lid in dl.downloaded_lists:
#    label=labels[lid]
#    NEs.append(pRead("{}neP{}.pickle".format(PDIR,label)))
#    print(label+"{0:.2f} for PICKLE loading evolved PCA structures".format(T.time()-TT)); TT=T.time()
##
### fazer vetor tridimensional de cada PCA
#VE1=[]
#VE2=[]
#VE3=[]
#VA1=[]
#VA2=[]
#VA3=[]
#labels1=["$cc$","$k$","$bt$","$\\lambda$"]
#labels2=["$cc$","$s$","$s^{in}$","$s^{out}$",
#         "$k$","$k^{in}$","$k^{out}$","$bt$","$\\lambda$"]
#labels3=["$cc$","$s$","$s^{in}$","$s^{out}$",
#         "$k$","$k^{in}$","$k^{out}$","$bt$",
#         "$asy$", "$\\mu^{asy}$","$\\sigma^{asy}$",
#         "$dis$","$\\mu^{dis}$","$\\sigma^{dis}$","$\\lambda$"]
#for lid, ne in zip(dl.downloaded_lists,NEs):
#    evec1=n.abs(n.array([pca.pca1.eig_vectors_ for pca in ne.networks_pcas]))
#    evec2=n.abs(n.array([pca.pca2.eig_vectors_ for pca in ne.networks_pcas]))
#    evec3=n.abs(n.array([pca.pca3.eig_vectors_ for pca in ne.networks_pcas]))
#    eval1=n.abs(n.array([ pca.pca1.eig_values_ for pca in ne.networks_pcas]))
#    eval2=n.abs(n.array([ pca.pca2.eig_values_ for pca in ne.networks_pcas]))
#    eval3=n.abs(n.array([ pca.pca3.eig_values_ for pca in ne.networks_pcas]))
#
#    VE1.append(evec1)
#    VE2.append(evec2)
#    VE3.append(evec3)
#
#    VA1.append(eval1)
#    VA2.append(eval2)
#    VA3.append(eval3)
#
#    m1= evec1.mean(0)
#    s1= evec1.std(0)
#    m1_=eval1.mean(0)
#    s1_=eval1.std(0)
#
#    m2= evec2[:,:,:3].mean(0)
#    s2= evec2[:,:,:3].std(0)
#    m2_=eval2[:,:3].mean(0)
#    s2_=eval2[:,:3].std(0)
#
#    m3= evec3[:,:,:3].mean(0)
#    s3= evec3[:,:,:3].std(0)
#    m3_=eval3[:,:3].mean(0)
#    s3_=eval3[:,:3].std(0)
#
#    # make table with each mean and std
#    #t1=n.zeros((m1.shape[0],6))
#    #t1[:,::2]=m1
#    #t1[:,1::2]=s1
#    #t1_=n.zeros(6)
#    #t1_[::2]=m1_
#    #t1_[1::2]=s1_
#    #tab_data=n.vstack((t1,t1_))
#    label=labels[lid]
#    tstring=g.pcaTable(labels1,m1,s1,m1_,s1_)
#    g.writeTex(tstring,TDIR+"tabPCA1{}.tex".format(label))
#    tstring=g.pcaTable(labels2,m2,s2,m2_,s2_)
#    g.writeTex(tstring,TDIR+"tabPCA2{}.tex".format(label))
#    tstring=g.pcaTable(labels3,m3,s3,m3_,s3_)
#    g.writeTex(tstring,TDIR+"tabPCA3{}.tex".format(label))
#
#    print(label+"{0:.2f} for making evolved PCA eigen vectors and values, 3d matrices and tex tables".format(T.time()-TT)); TT=T.time()
###
#### user activity
#### make that simple table and point to timelines
#### figure timelines of measures and other stuff
##AEs=[] # agent statistics
##for i, lid in enumerate(dl.downloaded_lists):
##    label=labels[lid]
##    ds=dss[i]
##    AEs.append(
##            g.AgentStatistics(ds))
##    # make .tex table
##    print(label+"{0:.2f} for agent statistics".format(T.time()-TT)); TT=T.time()
###
##data_=[]
##for i in order:
##    ae=AEs[i]
##    h_act="{:.2f}".format(ae.n_msgs_h_)
##    q1="{:.2f} ({:.2f}\\%)".format(ae.q1_*100,ae.Mq1*100)
##    q3="{:.2f} ({:.2f}\\%)".format(ae.q3_*100,ae.Mq3*100)
##    last_d10="{:.2f} (-{:.2f}\\%)".format(ae.last_d10_*100,ae.Mlast_d10*100)
##    data_.append([h_act,q1,q3,last_d10])
##labels_=["LAU","LAD","MET","CPP"]
##tstring=g.makeTables(labels_,data_)
##print(tstring)
##g.writeTex(tstring,TDIR+"userTab.tex")
##
##
#et=g.EvolutionTimelines(draw=False,label="LAU",tdir="./evoPCALAU/")
et=g.EvolutionTimelines(draw=False,label="LAU",tdir="./evoPCALAU/")
et.plotSingles()
#sizes=[50,100,250,500,1000,3300,9900]
##sizes=[4000,8000]
#order=[0,1] # CPP e LAD
#TDIR="evoTimelines"
#os.system("mkdir {}".format(TDIR))
#for size in sizes:
#    for listn in order:
#        lid=dl.downloaded_lists[listn]
#        label=labels[lid]
#        ds=dss[listn]
#        if size>=250:
#            step_size=size
#        else:
#            step_size=200
#        tdir="{}/evoTimeline{}-{}".format(TDIR,label,size)
#        ne=g.NetworkEvolution(window_size=size,step_size=step_size,tdir=tdir)
#        ne.evolveDataStructures(ds)
#        et=g.EvolutionTimelines(label=label,tdir=tdir+"/")
#
#
## Fazer figura com 3 plots:
## 1) grau x clust
## 2) PCA1
## 3) PCA2
#
#evo=pRead("evoPCALAU/im000000013.pickle")
##g.NetworkPCA(evo["nm"],g.NetworkPartitioning(evo["nm"],2,"degree"),tdir="evoPCALAU",tname="im13PCAPLOT.png",plot_sym=True)
#g.NetworkPCA(evo["nm"],g.NetworkPartitioning(evo["nm"],2,"degree"),tdir="/home/r/repos/stabilityInteraction/figs",tname="im13PCAPLOT__.png",plot_sym=True)

# EXTRA plots
#import pylab as p
#p.subplot(411)
#p.plot(tss[0].monthdays["samples"])
#p.subplot(412)
#p.plot(tss[1].monthdays["samples"])
#p.subplot(413)
#p.plot(tss[2].monthdays["samples"])
#p.subplot(414)
#p.plot(tss[3].monthdays["samples"])
#p.suptitle("CPP, LAD, LAU, MET list messages along the months")
#p.savefig(TDIR+"ActvityAlongMonthCycles.png")


# Facebook
#import social as S, os, networkx as x
#ENV=os.environ["PATH"]
#import  importlib
#from IPython.lib.deepreload import reload as dreload
#importlib.reload(S.utils)
##dreload(S)
#os.environ["PATH"]=ENV
#
## open 4 friendship networks
#fg= S.utils.GDFgraph("../extraData/RenatoFabbri06022014.gdf") # graph should be on fg.G
#fg2=S.utils.GDFgraph("../extraData/Massimo19062013.gdf") # graph should be on fg.G
#fg3=S.utils.GDFgraph("../extraData/DemocraciaDireta14072013.gdf") # graph should be on fg.G
#fg4=S.utils.GDFgraph("../extraData/SiliconValleyGlobalNetwork27042013.gdf") # graph should be on fg.G
#fg5=x.read_graphml("../extraData/amizadesParticipa.graphml") # graph should be on fg.G
#
## open 4 interaction networks
## use Social to parse gdfs
#fd= S.utils.GDFgraph("../extraData/SiliconValleyGlobalNetwork27042013_interactions.gdf") # graph should be on fg.G
#fd2= S.utils.GDFgraph("../extraData/SolidarityEconomy12042013_interactions.gdf") # graph should be on fg.G
#fd3= S.utils.GDFgraph("../extraData/DemocraciaDireta14072013_interacoes.gdf") # graph should be on fg.G
#fd4= S.utils.GDFgraph("../extraData/CienciasComFronteiras29032013_interacoes.gdf") # graph should be on fg.G
#fd5=x.read_graphml("../extraData/interacoesParticipa.graphml") # graph should be on fg.G
## Twitter
## make a retweet network or two
##tt= S.twitter.Twitter(app_key=            S.maccess.tw2.tak ,
##                      app_secret=         S.maccess.tw2.taks,
##                      oauth_token=        S.maccess.tw2.tat ,
##                      oauth_token_secret= S.maccess.tw2.tats)
##
##from twython import Twython
##tt2= Twython(app_key=            S.maccess.tw2.tak ,
##            app_secret=          S.maccess.tw2.taks,
##            oauth_token=         S.maccess.tw2.tat ,
##            oauth_token_secret=  S.maccess.tw2.tats)
#
#print("iniciando análise das redes de fb e tt")
##import pymongo, networkx as x
##from maccess import mdc
##client=pymongo.MongoClient(mdc.u2)
##db = client['sna']
##C = db["NEWarenaNETmundial"] #collection
##foo=C.find()
###foo=C.find({},{"id":1,"_id":0,"created_at":1}).sort("id",pymongo.ASCENDING) #twitterArena
##foo=C.find({},{"id":1,"_id":0,"user.screen_name":1,"text":1}) #twitterArena
##foo_=[i for i in foo]
##G,G_=S.utils.makeRetweetNetwork(foo_)
##F=[fg.G,fg2.G,fg3.G,fg4.G,fg5,fd.G,fd2.G,fd3.G,fd4.G,fd5,G,G_]
###F=[fd.G,fd2.G,fd3.G,fd4.G,G,G_]
##
### fazer o particionamento de erdos para todos eles, depois pca estático, fazer o q.
##
##def part(network):
##    class NetworkMeasures_:
##        pass
##    nm=nm=NetworkMeasures_()
##    nm.degrees=network.degree()
##    nm.nodes_= sorted(network.nodes(), key=lambda x : nm.degrees[x])
##    nm.degrees_=[nm.degrees[i] for i in nm.nodes_]
##    nm.edges=     network.edges(data=True)
##    nm.E=network.number_of_edges()
##    nm.N=network.number_of_nodes()
##    np=g.NetworkPartitioning(nm,10,metric="g")
##    return np
##parts=[]
##fracs=[]
##print("iniciando particionamentos")
##for net in F:
##    pp=part(net)
##    parts.append(pp)
##    ll=[len(i) for i in pp.sectorialized_agents__]
##    ll=[100*i/sum(ll) for i in ll]
##    fracs.append(ll)
##
##def pca(network):
##    class NetworkMeasures_:
##        pass
##    nm=nm=NetworkMeasures_()
##    nm.degrees=network.degree()
##    nm.nodes_= sorted(network.nodes(), key=lambda x : nm.degrees[x])
##    nm.degrees_=[nm.degrees[i] for i in nm.nodes_]
##
##    nm.gu=network.to_undirected()
##    if network.is_directed():
##        nm.weighted_directed_betweenness=x.betweenness_centrality(network,weight="weight")
##        nm.weighted_clusterings=x.clustering( nm.gu ,weight="weight")
##        nm.strengths=     network.degree(weight="weight")
##        nm.strengths_=[nm.strengths[i] for i in nm.nodes_]
##    else:
##        nm.weighted_directed_betweenness=x.betweenness_centrality(network)
##        nm.weighted_clusterings=x.clustering( nm.gu )
##    nm.weighted_directed_betweenness_=[
##      nm.weighted_directed_betweenness[i] for i in nm.nodes_]
##
##    nm.weighted_clusterings_=[nm.weighted_clusterings[i] for i in nm.nodes_]
##    if network.is_directed():
##        nm.in_degrees=network.in_degree()
##        nm.in_degrees_=[nm.in_degrees[i] for i in nm.nodes_]
##        nm.out_degrees=network.out_degree()
##        nm.out_degrees_=[nm.out_degrees[i] for i in nm.nodes_]
##        nm.in_strengths= network.in_degree(weight="weight")
##        nm.in_strengths_=[nm.in_strengths[i] for i in nm.nodes_]
##        nm.out_strengths=network.out_degree(weight="weight")
##        nm.out_strengths_=[nm.out_strengths[i] for i in nm.nodes_]
##
##    nm.edges=     network.edges(data=True)
##    nm.E=network.number_of_edges()
##    nm.N=network.number_of_nodes()
##
##
##    # symmetry measures
##    if network.is_directed():
##        nm.asymmetries=asymmetries=[]
##        nm.disequilibrium=disequilibriums=[]
##        nm.asymmetries_edge_mean=asymmetries_edge_mean=[]
##        nm.asymmetries_edge_std=asymmetries_edge_std=[]
##        nm.disequilibrium_edge_mean=disequilibrium_edge_mean=[]
##        nm.disequilibrium_edge_std=disequilibrium_edge_std=[]
##        for node in nm.nodes_:
##            if not nm.degrees[node]:
##                asymmetries.append(0.)
##                disequilibriums.append( 0.)
##                asymmetries_edge_mean.append(0.)
##                asymmetries_edge_std .append(0.)    
##                disequilibrium_edge_mean.append(0.)
##                disequilibrium_edge_std.append(0.)
##            else:
##                asymmetries.append(
##                    (nm.in_degrees[node]-nm.out_degrees[node])/nm.degrees[node])
##                disequilibriums.append( 
##                    (nm.in_strengths[node]-nm.out_strengths[node])/nm.strengths[node])
##                edge_asymmetries=ea=[]
##                edge_disequilibriums=ed=[]
##                predecessors=network.predecessors(node)
##                successors=  network.successors(node)
##                for pred in predecessors:
##                    if pred in successors:
##                        ea.append( 0. )
##                        ed.append((network[pred][node]['weight']-network[node][pred]['weight'])/nm.strengths[node])
##                    else:
##                        ea.append( 1. )
##                        ed.append(network[pred][node]['weight']/nm.strengths[node])
##                for suc in successors:
##                    if suc in predecessors:
##                        pass
##                    else:
##                        ea.append(-1.)
##                        ed.append(-network[node][suc]['weight']/nm.strengths[node])
##                asymmetries_edge_mean.append(   n.mean(ea))
##                asymmetries_edge_std .append(   n.std(ea))  
##                disequilibrium_edge_mean.append(n.mean(ed))
##                disequilibrium_edge_std.append( n.std(ed)) 
##    np=g.NetworkPCA(nm)
##    return np
##print("iniciando pcas")
##pcas=[]
##for net in F:
##    pp=pca(net)
##    pcas.append(pp)
##    print("+1pca de net de F")
##
##pDump(F,"pickledir/F.pickle")
##pDump(pcas,"pickledir/pcasFB-TW.pickle")
##for pa in parts: del pa.binomial
##pDump(parts,"pickledir/partsFB-TW.pickle")
##pDump(fracs,"pickledir/fracsFB-TW.pickle")
#pcas=pRead("pickledir/pcasFB-TW.pickle")
#parts=pRead("pickledir/partsFB-TW.pickle")
#fracs=pRead("pickledir/fracsFB-TW.pickle")
#F=pRead("pickledir/F.pickle")
#
##### Make tables with the fraction of participants in each erdos sector
## one and only table
##### Make one table for each pca of the networks each network
#labels_=["F1","F2","F3","F4","F5",
#        "I1","I2","I3","I4","I5",
#        "TT1","TT2"]
#
#for i, label in enumerate(labels_):
#    pca=pcas[i]
#    vals=n.vstack((pca.pca1.eig_vectors_,pca.pca1.eig_values_))
#    tstring=g.makeTables(labels1,vals)
#    g.writeTex(tstring,TDIR+"tabPCA1{}.tex".format(label))
#
## montar matriz de dados unica, 3 x nlistas = 27 colunas x 4 colunas
#NF = 5 # number of friendship networks
#NI = len(labels_)-NF # number of interaction networks
#nn=n.zeros((4,NF*3))
#for i in range(NF):
#    pca=pcas[i]
#    nn[:,i::NF]=n.abs(n.vstack((pca.pca1.eig_vectors_,pca.pca1.eig_values_)))
#
#tstring=g.makeTables(labels1,nn,True)
#g.writeTex(tstring,TDIR+"tabPCA1ExtraF.tex")
#
#nn_=n.zeros((4,NI*3))
#for i in range(NI):
#    pca=pcas[i+NF]
#    nn_[:,i::NI]=n.abs(n.vstack((pca.pca1.eig_vectors_,pca.pca1.eig_values_)))
#
#tstring=g.makeTables(labels1,nn_,True)
#g.writeTex(tstring,TDIR+"tabPCA1ExtraI.tex")
#
#
#
#nn2=n.zeros((9,len(labels_[5:])*3))
#for i in range(5,len(labels_)):
#    pca=pcas[i]
#    nn2[:,i-5::len(labels_[5:])]=n.abs(n.vstack((pca.pca2.eig_vectors_[:,:3],pca.pca2.eig_values_[:3])))
#tstring2=g.makeTables(labels2,nn2,True)
#g.writeTex(tstring2,TDIR+"tabPCA2Extra.tex")
#
#
#nn3=n.zeros((15,len(labels_[5:])*3))
#for i in range(5,len(labels_)):
#    pca=pcas[i]
#    nn3[:,i-5::len(labels_[5:])]=n.abs(n.vstack((pca.pca3.eig_vectors_[:,:3],pca.pca3.eig_values_[:3])))
#tstring3=g.makeTables(labels3,nn3,True)
#g.writeTex(tstring3,TDIR+"tabPCA3Extra.tex")
#
#tstring3=g.makeTables(labels_,n.array(fracs),True)
#g.writeTex(tstring3,TDIR+"tabSectorsExtra.tex")
#
#
## Tabela geral sobre cada lista com:
## sigla, proveniencia, critério para formação de aresta, dirigida ou nao, description, número de vertices, numero de arestas 
#data = [["F1", "Facebook","friendship","no","the friendship network of Renato Fabbri (author)",str(F[0].number_of_nodes()),str(F[0].number_of_edges())],
#        ["F2", "Facebook","friendship","no","the friendship network of Massimo Canevacci (senior anthropologist)",str(F[1].number_of_nodes()),str(F[1].number_of_edges())],
#        ["F3", "Facebook","friendship","no","the friendship network of a brazilian direct democracy group",str(F[2].number_of_nodes()),str(F[2].number_of_edges())],
#        ["F4", "Facebook","friendship","no","the friendship network of the Silicon Valley Global Network group",str(F[3].number_of_nodes()),str(F[3].number_of_edges())],
#        ["F5", "Participa.br","friendship","no","the friendship network of a brazilian federal social participation portal",str(F[4].number_of_nodes()),str(F[4].number_of_edges())],
#        ["I1", "Facebook","interaction","yes","the interaction network of the Silicon Valley Global Network group",str(F[5].number_of_nodes()),str(F[5].number_of_edges())],
#        ["I2", "Facebook","interaction","yes","the interaction network of a Solidarity Economy group",str(F[6].number_of_nodes()),str(F[6].number_of_edges())],
#        ["I3", "Facebook","interaction","yes","the interaction network of a brazilian direct democracy group",str(F[7].number_of_nodes()),str(F[7].number_of_edges())],
#        ["I4", "Facebook","interaction","yes","the interaction network of the 'Cience with Frontiers' group",str(F[8].number_of_nodes()),str(F[8].number_of_edges())],
#        ["I5", "Participa.br","interaction","yes","the interaction network of a brazilian federal social participation portal",str(F[9].number_of_nodes()),str(F[9].number_of_edges())],
#        ["TT1", "Twitter","retweet","yes","the retweet network of $\\approx 22k$ tweets with the hashtag \#arenaNETmundial",str(F[10].number_of_nodes()),str(F[10].number_of_edges())],
#        ["TT2", "Twitter","retweet","yes","same as TT1, but disconnected agents are not discarded",str(F[11].number_of_nodes()),str(F[11].number_of_edges())]]
#data_=[i[1:] for i in data]
#tstring3=g.makeTables(labels_,data_)
#g.writeTex(tstring3,TDIR+"tabExtra.tex")
#
##    evec1=n.abs(n.array([pca.pca1.eig_vectors_ for pca in ne.networks_pcas]))
##    eval1=n.abs(n.array([ pca.pca1.eig_values_ for pca in ne.networks_pcas]))
##    if "pca2" in dir(pca):
##    evec2=n.abs(n.array([pca.pca2.eig_vectors_ for pca in ne.networks_pcas]))
##    evec3=n.abs(n.array([pca.pca3.eig_vectors_ for pca in ne.networks_pcas]))
##    eval2=n.abs(n.array([ pca.pca2.eig_values_ for pca in ne.networks_pcas]))
##    eval3=n.abs(n.array([ pca.pca3.eig_values_ for pca in ne.networks_pcas]))
##
##    VE1.append(evec1)
##    VE2.append(evec2)
##    VE3.append(evec3)
##
##    VA1.append(eval1)
##    VA2.append(eval2)
##    VA3.append(eval3)
##
##    m1= evec1.mean(0)
##    s1= evec1.std(0)
##    m1_=eval1.mean(0)
##    s1_=eval1.std(0)
##
##    m2= evec2[:,:,:3].mean(0)
##    s2= evec2[:,:,:3].std(0)
##    m2_=eval2[:,:3].mean(0)
##    s2_=eval2[:,:3].std(0)
##
##    m3= evec3[:,:,:3].mean(0)
##    s3= evec3[:,:,:3].std(0)
##    m3_=eval3[:,:3].mean(0)
##    s3_=eval3[:,:3].std(0)
##
##    # make table with each mean and std
##    #t1=n.zeros((m1.shape[0],6))
##    #t1[:,::2]=m1
##    #t1[:,1::2]=s1
##    #t1_=n.zeros(6)
##    #t1_[::2]=m1_
##    #t1_[1::2]=s1_
##    #tab_data=n.vstack((t1,t1_))
##    label=labels[lid]
##    tstring=g.pcaTable(labels1,m1,s1,m1_,s1_)
##    g.writeTex(tstring,TDIR+"tabPCA1{}.tex".format(label))
##    tstring=g.pcaTable(labels2,m2,s2,m2_,s2_)
##    g.writeTex(tstring,TDIR+"tabPCA2{}.tex".format(label))
##    tstring=g.pcaTable(labels3,m3,s3,m3_,s3_)
##    g.writeTex(tstring,TDIR+"tabPCA3{}.tex".format(label))
##
##    print(label+"{0:.2f} for making evolved PCA eigen vectors and values, 3d matrices and tex tables".format(T.time()-TT)); TT=T.time()
#
#
## use the giant follower network I opened
##GG=x.DiGraph()
##with open("../extraData/Twitter-dataset/data/nodes.csv","r") as f:
##    nodes=f.read().split("\n")
##    GG.add_nodes_from(nodes)
##with open("../extraData/Twitter-dataset/data/edges.csv","r") as f:
##    edges=[i.split(",") for i in f.read().split("\n")]
##    GG.add_edges_from(edges)
#
## use one of the 2,7k tweets, the one with most users and edges
## (make a bundle of hashtags to find all 9 and get 24k msgs)
#
#
## finish twitter parser
#
## make a plot N x Gamma for 100 lists
