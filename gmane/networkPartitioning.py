import sys
from scipy import special, stats
from numpy import array as A
class NetworkPartitioning:
    network_count=0
    def __init__(self,networkMeasures=None, minimum_incidence=1,metric="strength"):
        if not networkMeasures:
            networkMeasures=g.NetworkMeasures()
        self.metric=metric
        metric_=self.standardizeName(metric)

        prob, max_degree_empirical, max_degree_possible = \
                self.basicMeasures( networkMeasures , metric_)

        incident_degrees, incident_degrees_, agent_degrees = \
                  self.makeDegreeLists( networkMeasures, metric_)

        empirical_distribution = self.makeEmpiricalDistribution(
            incident_degrees, incident_degrees_, networkMeasures.N )

        binomial_distribution=self.makeBinomialDistribution(
                   prob, max_degree_possible, incident_degrees_)

        binomial=stats.binom(max_degree_possible,prob)

        sectorialized_degrees= self.sectorializeDegrees(
         empirical_distribution, binomial_distribution, incident_degrees_)

        sectorialized_degrees_= self.newSectorializeDegrees(
         empirical_distribution, binomial_distribution, incident_degrees_)

        sectorialized_degrees__= self.newerSectorializeDegrees(
              empirical_distribution, binomial, incident_degrees_,
              max_degree_empirical,minimum_incidence,networkMeasures.N )

        sectorialized_agents= self.sectorializeAgents(
             sectorialized_degrees, networkMeasures.degrees)

        sectorialized_agents_= self.sectorializeAgents(
             sectorialized_degrees_, networkMeasures.degrees)

        sectorialized_agents__= self.sectorializeAgents(
             sectorialized_degrees__, agent_degrees)

        NetworkPartitioning.network_count+=1 # to keep track of how may partitions have been done

        self.makeSelf("incident_degrees_     ",incident_degrees_     ,
                      "incident_degrees     ",incident_degrees     ,
                      "sectorialized_agents  ",sectorialized_agents  ,
                      "sectorialized_agents_  ",sectorialized_agents_  ,
                      "sectorialized_agents__  ",sectorialized_agents__  ,
                      "sectorialized_degrees ",sectorialized_degrees ,
                      "sectorialized_degrees_ ",sectorialized_degrees_ ,
                      "sectorialized_degrees__ ",sectorialized_degrees__ ,
                      "binomial_distribution ",binomial_distribution ,
                      "prob"                  ,prob,
                      "max"                   ,(max_degree_possible, max_degree_empirical),
                      "empirical_distribution",empirical_distribution,
                      "binomial",binomial,
                      "metric_",metric_,
                      "minimum_incidence",minimum_incidence,
                      "binomial_distribution" ,binomial_distribution)

    def makeSelf(self, *args):
        for signifier, signified  in zip(args[::2], args[1::2]):
            #try:
                exec("self.{} = signified".format(signifier))
                #thing=signified
                #exec("self.{} = thing".format(signifier))
                #exec("self.{} = {}".format(signifier, signified))
                #exec("self.{} = ".format(signifier), signified)
            #except:
            #    self.binomial=signified
    def standardizeName(self,name):
        if name in (["s","strength","st"]+["f","força","forca","fo"]):
            name_="s"
        if name in (["d","degree","dg"]+["g","grau","gr"]):
            name_="d"
        return name_

    def basicMeasures(self,networkMeasures,metric_):
        nm=networkMeasures
        if metric_=="s":
            edge_weights=[i[2]["weight"] for i in nm.edges]
            average_edge_weight=sum(edge_weights)/nm.E
            max_degree_empirical=round(max(nm.strengths.values()) / average_edge_weight)
            max_degree_possible =2*(nm.N-1) # max d given N
            prob=nm.E/(nm.N*(nm.N-1)) # edge probability
            self.average_edge_weight=average_edge_weight
        elif metric_=="d":
            max_degree_empirical=max(nm.degrees.values())
            max_degree_possible=2*(nm.N-1) # max d given N
            prob=nm.E/(nm.N*(nm.N-1)) # edge probability
        return prob, max_degree_empirical, max_degree_possible
    def makeDegreeLists(self, networkMeasures,metric_):
        if metric_=="s":
            agent_degrees={i:round(j/self.average_edge_weight) for i,j in networkMeasures.strengths.items()}
            incident_degrees=[round(i/self.average_edge_weight) for i in networkMeasures.strengths.values()]
            incident_degrees_=list(set(incident_degrees))
            incident_degrees_.sort()
        elif metric_=="d":
            agent_degrees=networkMeasures.degrees
            incident_degrees=[i for i in networkMeasures.degrees.values()]
            incident_degrees_=list(set(incident_degrees))
            incident_degrees_.sort()
        return incident_degrees, incident_degrees_, agent_degrees
    def makeEmpiricalDistribution(self, incident_degrees, incident_degrees_, N):
        empirical_distribution=[]
        for degree in incident_degrees_:
            empirical_distribution.append(incident_degrees.count(degree)/N)
        return empirical_distribution
    def makeBinomialDistribution(self,prob,max_degree_possible,incident_degrees_):
        """If max_degree_possible == max_degree_empirical, makeBinomial ==1"""
        binomial_distribution=[] # occurance probability of degrees 
        for degree in incident_degrees_:
            if len(binomial_distribution) and binomial_distribution[-1]==0.0:
                binomial_distribution.append(0.0)
            else:
                n_occurrences=special.binom(max_degree_possible,degree)
                prob_degree=n_occurrences *  (prob**degree)*((1-prob)**(max_degree_possible-degree))
                binomial_distribution.append(prob_degree)
        return binomial_distribution

    def sectorializeAgents(self,sectorialized_degrees,agent_degrees):
        periphery=[x for x in agent_degrees
                     if agent_degrees[x] in sectorialized_degrees[0]]
        intermediary=[x for x in agent_degrees
                     if agent_degrees[x] in sectorialized_degrees[1]]
        hubs=[x for x in agent_degrees
                     if agent_degrees[x] in sectorialized_degrees[2]]
        return periphery, intermediary, hubs

    def newerSectorializeDegrees(self,empirical_distribution,binomial,incident_degrees_,max_degree_empirical,minimum_count,num_agents):
        # compute bins [start, end]
        prob_min=minimum_count/num_agents
        llimit=0
        rlimit=0
        self.bins=bins=[]
        self.empirical_probs=empirical_probs=[]
        while (rlimit < len(incident_degrees_)):
            if (sum(empirical_distribution[llimit:])>prob_min):
                prob_empirical=0
                while True:
                    prob_empirical=sum(
                         empirical_distribution[llimit:rlimit+1] )
                    if prob_empirical >= prob_min:
                        break
                    else:
                        rlimit+=1
                bins.append((llimit,rlimit))
                empirical_probs.append(prob_empirical)
                rlimit+=1
                llimit=rlimit
            else: # last bin
                print("last bin less probable than prob_min")
                rlimit=len(incident_degrees_)-1
                bins.append((llimit,rlimit))
                prob_empirical=sum(
                     empirical_distribution[llimit:rlimit+1] )
                empirical_probs.append(prob_empirical)
                rlimit+=1

        binomial_probs=[]
        for i, bin_ in enumerate(bins):
            llimit=bin_[0]
            rlimit=bin_[1]
            ldegree=incident_degrees_[llimit]-1
            rdegree=incident_degrees_[rlimit]
            binomial_prob=binomial.cdf(rdegree)-binomial.cdf(ldegree)
            binomial_probs.append(binomial_prob)

        # calcula probabilidades em cada bin
        # compara as probabilidades
        distribution_compare = list(A(empirical_probs) < A(binomial_probs))
        self.binomial_probs=binomial_probs
        self.distribution_compare0=distribution_compare
        tindex= distribution_compare.index(True)
        tindex2=distribution_compare[::-1].index(True)
        periphery_degrees=incident_degrees_[:tindex]
        intermediary_degrees=incident_degrees_[tindex:-tindex2]
        hub_degrees=         incident_degrees_[-tindex2:]
        return periphery_degrees, intermediary_degrees, hub_degrees

    def newSectorializeDegrees(self,empirical_distribution,binomial_distribution,incident_degrees_):
        distribution_compare = A(empirical_distribution) < A(binomial_distribution)
        self.distribution_compare=distribution_compare
        tindex= list(distribution_compare      ).index(True)
        tindex2=list(distribution_compare[::-1]).index(True)
        periphery_degrees=incident_degrees_[:tindex]
        intermediary_degrees=incident_degrees_[tindex:-tindex2]
        hub_degrees=         incident_degrees_[-tindex2:]
        return periphery_degrees, intermediary_degrees, hub_degrees
    def sectorializeDegrees(self,empirical_distribution,binomial_distribution,incident_degrees_):
        periphery_degrees=[]
        intermediary_degrees=[]
        hub_degrees=[]
        lock=0
        lock2=0
        for incident_prob, binomial_prob, degree in zip(
  empirical_distribution, binomial_distribution, incident_degrees_):
            if incident_prob < binomial_prob:
                intermediary_degrees.append(degree)
                lock=1
            elif (incident_prob > binomial_prob) and lock:
                hub_degrees.append(degree)

            else:
                periphery_degrees.append(degree)
        return periphery_degrees, intermediary_degrees, hub_degrees
"""
        self.perifericos=perifericos=[]
        self.intermediarios=intermediarios=[]
        self.hubs=hubs=[]
        self.quebras=quebras=[]
        setor="periferico"
        for grau in graus:
            prob_i=sum([o==grau for o in graus_incidentes])/len(ordenacao)
            if prob_i > 0:
                prob_r=pg[grau]
                incidente_maior=prob_i>=prob_r
                #print("\ngrau: %i; pi: %f; pr: %f; im: %i" % (grau, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA - grau",grau)
                        quebras.append("grau %i" % (grau,))
                        intermediarios+=hubs
                        hubs=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos.append(grau)
                elif setor == "intermediario":
                        intermediarios.append(grau)
                elif setor == "hub":
                    hubs.append(grau)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios)>0:
            self.g1=g1=intermediarios[0] # grau minimo dos intermediarios
            if len(hubs)>0:
                self.g2=g2=hubs[0] # grau minimo dos hubs
            else:
                print(u"DEGENERADO, não há hubs", "grau")
                self.g1=g1=0
                self.g2=g2=grau_max+1
        else:
            print(u"DEGENERADO, não há intermediário", "grau")
            # ajustando de forma que sejam todos intermediários
            self.g1=g1=0 # grau minimo dos intermediarios
            self.g2=g2=grau_max +1# grau minimo dos hubs

# contando os vertices em cada setor
        n_perifericos=sum([gi<g1 for gi in graus_incidentes])
        n_intermediarios=sum([gi<g2 for gi in graus_incidentes])-n_perifericos
        n_hubs=g.number_of_nodes()-(n_perifericos+n_intermediarios)
        self.dist=(n_perifericos,n_intermediarios,n_hubs)
"""
