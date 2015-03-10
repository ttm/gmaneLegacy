import sys
from scipy import special
class NetworkPartitioning:
    network_count=0
    def __init__(self,networkMeasures=None):
        if not networkMeasures:
            networkMeasures=g.NetworkMeasures()

        prob, max_degree_empirical, max_degree_possible = \
                self.basicMeasures( networkMeasures )

        incident_degrees, incident_degrees_ = \
                  self.makeDegreeLists( networkMeasures)

        empirical_distribution = self.makeEmpiricalDistribution(
            incident_degrees, incident_degrees_, networkMeasures.N )

        binomial_distribution=self.makeBinomialDistribution(
                   prob, max_degree_possible, incident_degrees_)

        sectorialized_degrees= self.sectorializeDegrees(
         empirical_distribution, binomial_distribution, incident_degrees_)

        sectorialized_agents= self.sectorializeAgents(
             sectorialized_degrees, networkMeasures.degrees)
        NetworkPartitioning.network_count+=1 # to keep track of how may partitions have been done

        self.incident_degrees_=incident_degrees_
        self.sectorialized_agents =sectorialized_agents 
        self.sectorialized_degrees=sectorialized_degrees
        self.binomial_distribution=binomial_distribution
        self.empirical_distribution=empirical_distribution


    def basicMeasures(self,networkMeasures):
        nm=networkMeasures
        max_degree_empirical=max(nm.degrees.values())
        max_degree_possible=2*(nm.N-1) # max d given N
        prob=nm.E/(nm.N*(nm.N-1)) # edge probability
        return prob, max_degree_empirical, max_degree_possible
    def makeDegreeLists(self, networkMeasures):
        incident_degrees=[i for i in networkMeasures.degrees.values()]
        incident_degrees_=list(set(networkMeasures.degrees.values()))
        incident_degrees_.sort()
        return incident_degrees, incident_degrees_
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
    def sectorializeDegrees(self,empirical_distribution,binomial_distribution,incident_degrees_):
        periphery_degrees=[]
        intermediary_degrees=[]
        hub_degrees=[]
        lock=0
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
