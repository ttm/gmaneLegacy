import sys
import collections as c
from scipy import special, stats
from numpy import array as A, linspace, sin, pi as PI, hstack, vstack
import pylab as p, networkx as x

class NetworkDrawer:
    drawer_count=0
    def __init__(self,metric="strength"):
        self.drawer_count+=1
        metric_=self.standardizeName(metric)
        self.metric_=metric_

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
            measures_=network_measures.degree
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

    def drawNetwork(self,network,network_measures):
        p.clf()

        in_measures=network_measures.in_strengths
        min_in=max(in_measures.values())/3+0.1
        out_measures=network_measures.out_strengths
        min_out=max(out_measures.values())/3+.1

        clustering=network_measures.weighted_clustering
        A=x.to_agraph(network.g)
        A.node_attr['style']='filled'
        A.graph_attr["bgcolor"]="black"
        A.graph_attr["pad"]=.1
        A.graph_attr["size"]="9.5,12"
        cm=p.cm.Reds(range(2**10)) # color table
        nodes=A.nodes()
        ii=0
        colors=[]
        for node in nodes:
            n_=A.get_node(node)
            ind_author=self.authors.index(n_)
            n_.attr['fillcolor']= '#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
            n_.attr['fixedsize']=True
            n_.attr['width']=  abs(.07*(in_measures[n_]/min_in+0.5))
            n_.attr['height']= abs(.07*(out_measures[n_]/min_out+0.5))
            pos="%f,%f"%tuple(self.posXY[ind_author]); ii+=1
            n_.attr["pos"]=pos
            n_.attr["pin"]=True
            n_.attr["fontsize"]=15
            n_.attr["fontcolor"]="white"
            colors.append('#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]]))

        weights=[s[2]["weight"] for s in network_measures.edges]
        self.weights=weights
        max_weight=max(weights)
        self.max_weight=max_weight
        self.weights_=[]
        edges=A.edges()
        for e in edges:
            factor=float(e.attr['weight'])
            self.weights_.append(factor)
            e.attr['penwidth']=.2*factor
            e.attr["arrowsize"]=.5
            e.attr["arrowhead"]="lteeoldiamond"
            w=factor/max_weight # factor em [0-1]

            cor=p.cm.Spectral(int(w*255))
            self.cor=cor
            cor256=255*A(cor[:-1])

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

        label="imagem: %i, |g|= %i, |e|= %i"%(10,network_measures.N,network_measures.E)
        A.graph_attr["label"]=label

        A.graph_attr["fontcolor"]="white"
        #A.draw('%s' % (nome,)) # twopi ou circo
        A.draw('%s.png' % ("example",), prog="neato") # twopi ou circo
        print('scrita figura: %s' % (nome,)) # printando nome
        ################
        # remoção de todos os vertices auxiliares
        self.A=A



    def updateNetwork(self,network,networkMeasures=None):
        pass
    def makeXY(self):
        size_periphery=self.k1
        size_intermediary=self.k2-self.k1
        size_hubs=self.network_measures.N-self.k2

        xh=linspace(0,0.5,endpoint=True)
        thetah=2*PI*xh
        yh=sin(thetah)

        xi=linspace(1,0.5, endpoint=False)[::-1]
        thetai=2*PI*xi
        yi=sin(thetai)

        xp=linspace(.95,0.4)
        yp=linspace(.1,1.25)

        self.pos=((xp,yp),(xi,yi),(xh,yh))
        self.posX=posX=hstack((xp,xi,xh))
        self.posY=posY=hstack((yp,yi,yh))
        self.posXY=vstack((posX.T,posY.T)).T
        # use with self.authors and self.measures
        p.clf()
        p.plot(posX,posY)
        p.savefig("numberMarkerSubmarkerCountInfo.png")
