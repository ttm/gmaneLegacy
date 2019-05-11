import musicLegacy as m, numpy as n, os, pickle
from .networkPartitioning import *
UTILS=m.Utils()
bt=m.BasicTables()
co=m.BasicConverter()
sy=m.Synth()
sy.adsrSetup(A=20,D=20,R=10)
#sy.tab=sy.tables.square
sy2=m.pieces.FourHubsDance()
sy2.sy=sy

class EvolutionMusic:
    """Make music for appreciation of network evolution"""
    def __init__(self,tdir="./evolution/",label="gmaneID",samplerate=44100):
        self.sy=sy
        self.sy2=sy2
        self.m=m
        self.samplerate=samplerate
        self.tdir=tdir
        self.label=label
        self.getMeasures()
        self.makeMusic()
    def makeMusic(self,framerate=4.,renderVideo=True):
        """Make music with 4 frames tempo"""
        self.dur_frame=1/framerate
        self.T=4*self.dur_frame
        # frames per pulse

        # 4 notas por tempo, uma para cada um dos hubs
        agents=self.overall[1][-2].nodes__[-4:]
        # observa os graus dos 4
        #self.degrees=n.array([[nm.degrees.get(agent,0) for nm in self.agents["nm"]] for agent in agents])
        self.degrees=n.array([[nm.strengths.get(agent,0) for nm in self.agents["nm"]] for agent in agents])
        self.n_frames=self.degrees.shape[1]

        total_time=self.n_frames/framerate

        # normaliza cada
        self.amb=12
        self.off=[0,12,24,36][::-1]
        self.degrees_=((n.subtract(self.degrees.T,self.degrees.min(1)) / (self.degrees.max(1)-self.degrees.min(1))).T)
        self.degrees__=(self.degrees_.T+self.off).T

        self.sy2.setupEngine(self.samplerate,total_time,self.T)
        line1=self.sy2.sonicLine2(
   self.degrees_[-1],tmean=.3)
        line2=self.sy2.sonicLine2(
   self.degrees_[-2],tmean=.7,DUR=1)

        sy.adsrSetup(A=5,D=20,S=-20,R=100)
        sy.tab=sy.tables.square
        line4=self.sy2.sonicLine1(
  self.degrees_[0],[0,2,4,6,8,10],ambit=12,rythmic_pattern=[0,0,1,1],f0=440)
        sy.adsrSetup(A=5,D=20,S=-15,R=730)
        # Adicionar vibrato proporcional
        sy.tab=sy.tables.saw
        line3=self.sy2.sonicLine1(
    self.degrees_[1],[0,2,4,6,8,10],ambit=12,rythmic_pattern=[1],f0=110)

        #UTILS.write(line2+line3[:len(line2)]+line4,"mixY.wav")
        llen=len(line4)
        UTILS.write(line1[:llen]+
                    line2[:llen]+
                    line3[:llen]+
                    line4[:llen],self.tdir+"mixY.wav")
        # coloca cada um em uma oitava e escala
        # une os vetores de frequencia
        # junta duração
        #self.midi_notes=n.hstack(self.degrees__.T)

        # fundo feito pelos perifericos
        # buscar alguma sonoridade ruidosa para os intermediarios 

        #self.n_frames=len(self.agents["nm"])
        #self.freqs=co.p2f(110,[[0,7][i%2] for i in range(self.n_frames)])
        #self.freqs=co.p2f(110,self.midi_notes[::4])
        #self.durs=[self.dur_frame]*self.n_frames
        #self.notes=[sy.render(f,d) for f,d in zip(self.freqs,self.durs)]
        #UTILS.write(n.hstack(self.notes),"notes.wav")

        #self.freqs2=co.p2f(110,self.midi_notes[2::12])
        #self.durs2=[self.dur_frame*3]*(self.n_frames//3)
        #self.notes2=[sy.render(f,d) for f, d in zip(self.freqs2, self.durs2)]
        #UTILS.write(n.hstack(self.notes2),"notes2.wav")

        #mix=n.hstack(self.notes)+n.hstack(self.notes2)

        #UTILS.write(mix,"mix.wav")
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
                "exc":[],
                "inc":[],
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
                agents["inc"].append(compound["inc"])
        self.agents=agents
