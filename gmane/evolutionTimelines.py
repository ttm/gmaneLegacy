import pylab as p, os, pickle
from .networkPartitioning import *

class EvolutionTimelines:
    def __init__(self,tdir="./evolution/"):
        filenames=os.listdir(tdir)
        filenames_=[i for i in filenames if i.endswith(".pickle")]
        filenames_=[i for i in filenames_ if i.startswith("im")]
        filenames_.sort()
        self.getMeasures(filenames_,tdir)
        self.drawTimelines()
    def getMeasures(self,filenames_,tdir):
        fractions=[]
        agents={"s":[],"is":[],"os":[],
                "d":[],"id":[],"od":[]}
        for filename in filenames_:
            with open(tdir+filename,"rb") as f:
                data=pickle.load(f)
                nm=data["nm"]
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
        self.fractions=fractions
        self.agents=agents
                

    def drawTimelines(self):
        pass

