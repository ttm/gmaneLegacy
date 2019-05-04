import sys
import collections as c
from scipy import special, stats
import numpy as n, pylab as p, networkx as x

class NetworkDrawer:
    drawer_count=0
    def __init__(self,metric="strength"):
        self.drawer_count+=1
        metric_=self.standardizeName(metric)
        self.metric_=metric_
        self.draw_count=0

    def standardizeName(self,name):
        if name in (["s","strength","st"]+["f","força","forca","fo"]):
            name_="s"
        if name in (["d","degree","dg"]+["g","grau","gr"]):
            name_="d"
        return name_
    def makeLayout(self,network_measures,network_partitioning=None):
        """Delivers a sequence of user_ids and (x,y) pos.
        """
        self.network_measures=network_measures
        if self.metric_=="s":
            measures_=network_measures.strengths
        elif self.metric_=="d":
            measures_=network_measures.degrees
        else:
            print("not known metric to make layout")
        self.ordered_measures=ordered_measures = c.OrderedDict(sorted(measures_.items(), key=lambda x: x[1]))
        self.measures=measures=list(ordered_measures.values())
        self.authors=authors=  list(ordered_measures.keys())
        total=network_measures.N
        if not network_partitioning:
            self.k1=k1=round(total*.80)
            self.k2=k2=round(total*.95)
            self.periphery=authors[:k1]
            self.intermediary=authors[k1:k2]
            self.hubs=authors[k2:]
        else:
            sectors=network_partitioning.sectorialized_agents__
            self.k1=k1=len(sectors[0])
            self.k2=k2=k1+len(sectors[1])
            self.periphery,self.intermediary,self.hubs=sectors
        print("fractions ={:0.4f}, {:0.4f}, {:0.4f}".format(k1/total, (k2-k1)/total, 1-k2/total))
        self.makeXY()

    def drawNetwork(self, network,network_measures,filename="example.png",label="auto",network_partitioning=None):
        p.clf()

        if self.metric_=="s":
            measures_=network_measures.strengths
        elif self.metric_=="d":
            measures_=network_measures.degree
        else:
            print("not known metric to make layout")
        ordered_measures = c.OrderedDict(sorted(measures_.items(), key=lambda x: x[1]))
        measures=list(ordered_measures.values())
        authors=  list(ordered_measures.keys())

        total=network_measures.N
        if not network_partitioning:
            k1=k1=round(total*.80)
            k2=k2=round(total*.95)
            periphery=authors[:k1]
            intermediary=authors[k1:k2]
            hubs=authors[k2:]
        else:
            sectors=network_partitioning.sectorialized_agents__
            k1=k1=len(sectors[0])
            k2=k2=k1+len(sectors[1])
            periphery,intermediary,hubs=(set(iii) for iii in sectors)

        in_measures=network_measures.in_strengths
        min_in=max(in_measures.values())/3+0.1
        out_measures=network_measures.out_strengths
        min_out=max(out_measures.values())/3+.1

        self.clustering=clustering=network_measures.weighted_clusterings
        A=x.drawing.nx_agraph.to_agraph(network.g)
        A.node_attr['style']='filled'
        A.graph_attr["bgcolor"]="black"
        A.graph_attr["pad"]=.1
        #A.graph_attr["size"]="9.5,12"
        A.graph_attr["fontsize"]="25"
        if label=="auto":
            label=self.makeLabel()
        A.graph_attr["label"]=label
        A.graph_attr["fontcolor"]="white"
        cm=p.cm.Reds(range(2**10)) # color table
        self.cm=cm
        nodes=A.nodes()
        self.colors=colors=[]
        self.inds=inds=[]
        self.poss=poss=[]
        for node in nodes:
            n_=A.get_node(node)
            ind_author=self.authors.index(n_)
            inds.append(inds)
            colors.append(        '#%02x%02x%02x' % tuple([int(255*i) for i in cm[int(clustering[n_]*255)][:-1]]))
            #n_.attr['fillcolor']= '#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
            n_.attr['fillcolor']= colors[-1]
            n_.attr['fixedsize']=True
            n_.attr['width']=  abs(.6*(in_measures[n_]/min_in+  .05))
            n_.attr['height']= abs(.6*(out_measures[n_]/min_out+.05))
            if n_ in hubs:
                n_.attr["shape"] = "hexagon"
            elif n_ in intermediary:
                pass
            else:
                n_.attr["shape"] = "diamond"
            pos="%f,%f"%tuple(self.posXY[ind_author])
            poss.append(pos)
            n_.attr["pos"]=pos
            n_.attr["pin"]=True
            n_.attr["fontsize"]=25
            n_.attr["fontcolor"]="white"
            n_.attr["label"]=""

        weights=[s[2]["weight"] for s in network_measures.edges]
        self.weights=weights
        max_weight=max(weights)
        self.max_weight=max_weight
        self.weights_=[]
        edges=A.edges()
        for e in edges:
            factor=float(e.attr['weight'])
            self.weights_.append(factor)
            e.attr['penwidth']=.34*factor
            e.attr["arrowsize"]=1.5
            e.attr["arrowhead"]="lteeoldiamond"
            w=factor/max_weight # factor em [0-1]

            cor=p.cm.Spectral(int(w*255))
            self.cor=cor
            cor256=255*n.array(cor[:-1])

            r0=int(cor256[0]/16)
            r1=int(cor256[0]-r0*16)
            r=hex(r0)[-1]+hex(r1)[-1]

            g0=int(cor256[1]/16)
            g1=int(cor256[1]-g0*16)
            g=hex(g0)[-1]+hex(g1)[-1]

            b0=int(cor256[2]/16)
            b1=int(cor256[2]-b0*16)
            b=hex(b0)[-1]+hex(b1)[-1]

            #corRGB="#"+r+g+b+":#"+r+g+b
            corRGB="#"+r+g+b

            e.attr["color"]=corRGB

        A.draw(filename, prog="neato") # twopi ou circo
        ################
        self.A=A
        self.draw_count+=1
    def makeLabel(self):
        label=""
        if "window_size" in dir(self):
            label+="w: {}, ".format(self.window_size)
            #m: %i, N = %i, E = %i"%(self.draw_count*self.step_size,self.network_measures.N,self.network_measures.E)
        if "step_size" in dir(self):
            label+="m: {} ,".format(self.draw_count*self.step_size+self.offset)
        else:
            label+="m: %i, ".format(self.draw_count)
            #self.network_measures.N,self.network_measures.E)
        label+="N = %i, E = %i"%(self.network_measures.N,self.network_measures.E)
        return label

    def updateNetwork(self,network,networkMeasures=None):
        pass
    def makeXY(self):
        size_periphery=self.k1
        size_intermediary=self.k2-self.k1
        size_hubs=self.network_measures.N-self.k2
        if size_hubs%2==1:
            size_hubs+=1
            size_intermediary-=1
        xh=n.linspace(0,0.5,size_hubs,endpoint=False)[::-1]
        thetah=2*n.pi*xh
        yh=n.sin(thetah)

        xi=n.linspace(1,0.5, size_intermediary, endpoint=True)
        thetai=2*n.pi*xi
        yi=n.sin(thetai)

        xp=n.linspace(.95,0.4, size_periphery)[::-1]
        yp=n.linspace(.1,1.25, size_periphery)[::-1]

        self.pos=((xp,yp),(xi,yi),(xh,yh))
        XFACT=7
        YFACT=3
        self.posX=posX=n.hstack((xp,xi,xh))*XFACT
        self.posY=posY=n.hstack((yp,yi,yh))*YFACT
        self.posXY=n.vstack((posX.T,posY.T)).T
