import pickle, os
from .listDataStructures import *
from .interactionNetwork import *
from .networkMeasures import *
from .networkPartitioning import *
from .networkDrawer import *
from .agentStatistics import *
from .timeStatistics import *
from .pca import *
class NetworkEvolution:
    def __init__(self, window_size=200, step_size=3, make_analysis=True, write_analysis=True, make_pca=True, write_pca=True):
        self.window_size=window_size
        self.step_size=step_size
        self.make_analysis=make_analysis
        self.write_analysis=write_analysis
        self.make_pca      =make_pca
        self.write_pca     =write_pca
    def evolveRaw(self, loaded_messages,offset=0,tdir="evolution",clean_dir=True,print_status=True,imagerate=18,erdos_sectors=True,minimum_incidence=2):
        if len(loaded_messages)<self.window_size:
            raise ValueError("incoming messages smaller than window_size [({}-{})/{}]".format(
                len(loaded_messages), offset, self.window_size))
        pointer=offset
        self.offset=offset
        self.minimum_incidence=minimum_incidence
        self.tdir=tdir
        counter=0

        if tdir: os.system("mkdir {}".format(tdir))
        if clean_dir: os.system("rm {}/*".format(tdir))
        while pointer+self.window_size<len(loaded_messages):
            messages=loaded_messages[pointer:pointer+self.window_size]

            ds=ListDataStructures(messages)
            ts=TimeStatistics(ds)
            ps=AgentStatistics(ds)
            iN=InteractionNetwork(ds)
            nm=NetworkMeasures(iN)
            np=NetworkPartitioning(nm,minimum_incidence)
            npca=NetworkPCA(nm,np,tdir=tdir,tname="pca{:09}".format(counter))
            del np.binomial
            with open("{}/im{:09}.pickle".format(tdir,counter),"wb") as f:
                tall=dict(ds=ds,ts=ts,ps=ps,iN=iN,nm=nm,
                        agents=np.sectorialized_agents__,
                        minimum_incidence=np.minimum_incidence,
                        np=np,
                        npca=npca)
                pickle.dump(tall,f)
            if "drawer" not in dir(self):
                print("runing self.setDrawer to enable images and movie")
                self.setDrawer(loaded_messages,tdir=tdir)
            label="T{}W{}S{}R{}M{}N{}E{}".format(
                len(loaded_messages), self.window_size, self.step_size, 
                imagerate, pointer,nm.N,nm.E)
            self.drawer.drawNetwork( iN,nm ,"{}/im{:09}.png".format(tdir,counter), label,np)
            if print_status:
                print("analysed {}-{} / {}".format(
                    pointer,pointer+self.window_size,len(loaded_messages)))
            pointer+=self.step_size
            counter+=1
            # make pca 
            # write pca with cpickle
        self.saveOverallInfo()
        videoname="evoT{}W{}O{}S{}R{}".format(
                len(loaded_messages), self.window_size, offset, self.step_size, imagerate)
        self.makeVideo(tdir,videoname,imagerate)
    def saveOverallInfo(self):
        with open("{}/overallInfo.pickle".format(self.tdir),"wb") as f:
            tdict=dict( window_size=self.window_size,
                         step_size =self.step_size,
                            offset =self.offset,
                  minimum_incidece =self.minimum_incidence )
            del self.overall[-1].binomial
            pickle.dump((tdict,self.overall),f)

    def makeVideo(self,tdir="evolution",videoname="fooname",imagerate=18):
        command="avconv -f image2 -framerate {} -i {}/im%09d.png -qscale 1 -b 65536k -y {}/{}.avi".format(
                imagerate, tdir, tdir, videoname)
        os.system(command)
    def setDrawer(self,messages=None,network_measures=None, network_partitioning=None,tdir="."):
        if messages:
            ds=ListDataStructures(messages)
            ts=TimeStatistics(ds)
            ps=AgentStatistics(ds)
            iN=InteractionNetwork(ds)
            nm=NetworkMeasures(iN)
            np=NetworkPartitioning(nm,3)
        else:
            print("under construction")
        drawer=NetworkDrawer()
        drawer.makeLayout(nm,np)
        drawer.drawNetwork(iN,nm,"{}/overall.png".format(tdir))
        drawer.step_size=self.step_size
        drawer.offset=self.offset
        drawer.window_size=self.window_size
        self.drawer=drawer
        self.drawer=drawer
        self.overall=(ds,ts,ps,iN,nm,np)

