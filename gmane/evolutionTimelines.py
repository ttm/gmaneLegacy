import pylab as p, matplotlib, os, pickle
from .networkPartitioning import *

class EvolutionTimelines:
    def __init__(self,tdir="./evolution/",label="gmaneID"):
        self.tdir=tdir
        self.label=label
        self.getMeasures()
        self.drawTimelines()
    def getOverallMeasures(self):
        filenames=os.listdir(self.tdir)
        filenames_=[i for i in filenames if i.endswith(".pickle")]
        filename=[i for i in filenames_ if "overall" in i][0]
        with open(self.tdir+filename,"rb") as f:
                self.overall=pickle.load(f)
    def getMeasures(self):
        self.getOverallMeasures()
        filenames=os.listdir(self.tdir)
        filenames_=[i for i in filenames if i.endswith(".pickle")]
        filenames_=[i for i in filenames_ if i.startswith("im")]
        filenames_.sort()
        agents={"s":[],"is":[],"os":[],
                "d":[],"id":[],"od":[],
                "exc":[],"excc":[],"exce":[],
                "inc":[],"incc":[],"ince":[],
                "nm":[]}
        for filename in filenames_:
            with open(self.tdir+filename,"rb") as f:
                data=pickle.load(f)
                nm=data["nm"]
                agents["nm"].append(nm)
                n_agents=nm.N
                minimum_incidence=data["np"].minimum_incidence
                agents["s"].append(data["np"].sectorialized_agents__)
                agents["is"].append(
                        NetworkPartitioning(nm,minimum_incidence=minimum_incidence,metric="is").sectorialized_agents__ )
                agents["os"].append(
                        NetworkPartitioning(nm,minimum_incidence=minimum_incidence,metric="os").sectorialized_agents__ )
                agents["d"].append(
                        NetworkPartitioning(nm,minimum_incidence=minimum_incidence,metric="d").sectorialized_agents__ )
                agents["id"].append(
                        NetworkPartitioning(nm,minimum_incidence=minimum_incidence,metric="id").sectorialized_agents__ )
                agents["od"].append(
                        NetworkPartitioning(nm,minimum_incidence=minimum_incidence,metric="od").sectorialized_agents__ )
                # pegar os agentes da rede em
                # todos os outros critérios de particionamento simples:
                # d, id, od, is, os
                # e mandar eles para uma função que já calcula
                # os particionamentos compostos
                compound=compoundPartitioning(agents)
                agents["exc"].append(compound["exc"])
                agents["excc"].append(compound["excc"])
                agents["exce"].append(compound["exce"])
                agents["inc"].append(compound["inc"])
                agents["incc"].append(compound["incc"])
                agents["ince"].append(compound["ince"])
        self.agents=agents
    def plotFracs(self,ttype,subplot,ate,step_size):
        p.subplot(subplot)
        p.title(ttype)
        if ttype == "degree": ttype_="d"
        if ttype == "strength": ttype_="s"
        if ttype == "in-degree": 
            ttype_="id"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "out-degree": ttype_="od"
        if ttype == "in-strength": 
            ttype_="is"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "out-strength": ttype_="os"
        if ttype == "exclusivist": ttype_="exc"
        if ttype == "inclusivist": ttype_="inc"
        if ttype == "exclusivist cascade": 
            ttype_="excc"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "inclusivist cascade": 
            ttype_="incc"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "exclusivist externals": 
            ttype_="exce"
            p.xlabel(r"messages $\rightarrow$")
        if ttype == "inclusivist externals": 
            ttype_="ince"
            p.xlabel(r"messages $\rightarrow$")
        fractions=[fractionLengths(i) for i in self.agents[ttype_]]
        hubs_fractions=[i[2] for i in fractions]
        intermediary_fractions=[i[1] for i in fractions]
        periphery_fractions=[i[0] for i in fractions]

        p.plot(list(range(0,ate,step_size)),periphery_fractions,"b")
        p.plot(list(range(0,ate,step_size)),intermediary_fractions,"g")
        p.plot(list(range(0,ate,step_size)),hubs_fractions,"r")
        p.ylim(0,1)
        p.xlim(-5,ate+5)
    def plotMeasure(self,title,subplot,ate,step_size):
        if subplot=="5,2,10":
            p.subplot(5,2,10)
        else:
            p.subplot(subplot)
        p.title(title)
        if title=="total weight":
            measures=[sum([i[2]["weight"] for i in nm.edges])
                    for nm in self.agents["nm"]]
            p.ylabel(r"$\sum s_i \;\;\rightarrow$")
        elif title=="number of edges":
            measures=[i.E for i in self.agents["nm"]]
            #p.ylabel(r"$\mathfrak{z} \rightarrow$",fontsize=20)
            p.ylabel(r"$z \rightarrow$",fontsize=20)
        elif title=="number of vertices":
            measures=[i.N for i in self.agents["nm"]]
            p.xlabel(r"messages $\rightarrow$")
            p.ylabel(r"N $\rightarrow$")
        elif title=="center, periphery and discon.":
            center=[len(i.center) for i in self.agents["nm"]]
            p.plot(range(0,ate,step_size),center,"b")
            periphery=[len(i.periphery) for i in self.agents["nm"]]
            p.plot(range(0,ate,step_size),periphery,"k",linestyle="dashed")
            periphery_=[len(i.periphery_) for i in self.agents["nm"]]
            measures=[i+j for i,j in zip(periphery,periphery_)]
            p.xlabel(r"messages $\rightarrow$")
            p.ylabel("number of\nnodes"+r"$\rightarrow$")

        p.plot(range(0,ate,step_size),measures,"k")
        p.ylim(min(measures)*.99,max(measures)*1.01)
        p.xlim(-5,ate+5)


    def plotFirstPage(self):
        p.clf()
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(7.,8.4)
        step_size=self.overall[0]["step_size"]
        ate=self.overall[1][0].n_messages-self.overall[0]["window_size"]
        p.suptitle("Primary divisions. Window: %i messages.\nPlacement resolution: %i messages. %s" % (self.overall[0]["window_size"],step_size,self.label))
        self.plotFracs("degree","521",ate,step_size)
        self.plotFracs("strength","522",ate,step_size)
        self.plotFracs("in-degree","523",ate,step_size)
        self.plotFracs("in-strength","524",ate,step_size)
        self.plotFracs("out-degree","525",ate,step_size)
        self.plotFracs("out-strength","526",ate,step_size)
        self.plotMeasure("total weight","527",ate,step_size)
        self.plotMeasure("number of edges","528",ate,step_size)
        self.plotMeasure("number of vertices","529",ate,step_size)
        self.plotMeasure("center, periphery and discon.","5,2,10",ate,step_size)
        p.subplots_adjust(left=0.105,bottom=0.05,right=0.98,top=0.9,wspace=0.28,hspace=0.69)
        filename="{}-W{}-S{}.png".format(self.label,self.overall[0]["window_size"],step_size)
        p.savefig("{}/{}".format(self.tdir,filename))
        # simple plot:
        p.clf()
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(7.,5.4)
        p.suptitle("Compound divisions. Window: %i messages.\nPlacement resolution: %i messages. %s" % (self.overall[0]["window_size"],step_size,self.label))
        self.plotFracs("exclusivist","321",ate,step_size)
        self.plotFracs("inclusivist","322",ate,step_size)
        self.plotFracs("exclusivist cascade","323",ate,step_size)
        self.plotFracs("inclusivist cascade","324",ate,step_size)
        self.plotFracs("exclusivist externals","325",ate,step_size)
        self.plotFracs("inclusivist externals","326",ate,step_size)
        p.subplots_adjust(left=0.09,bottom=0.08,right=0.99,top=0.86,wspace=0.28,hspace=0.55)
        filename="{}-W{}-S{}_.png".format(self.label,self.overall[0]["window_size"],step_size)
        p.savefig("{}/{}".format(self.tdir,filename))

    def drawTimelines(self):
        self.plotFirstPage()

def fractionLengths(list_of_lists):
    llist=[len(i) for i in list_of_lists]
    total=sum(llist)
    return [i/total for i in llist]
