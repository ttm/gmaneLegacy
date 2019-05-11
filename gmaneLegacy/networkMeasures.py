import networkx as x, time as t, numpy as n
class NetworkMeasures:
    """Extracts measures for incoming network.

    Both overall measures and measures of each vertex are taken.
    """
    def __init__(self,network=None,exclude=["unweghted_undirected_betweenness","weighted_undirected_betweenness","unweighted_directed_betweenness", "rich_club"]):
        if not network:
            network=g.InteractionNetwork()

        #_all=["clustering"] # measures taken from graph by a method of itself
        #_all_=[] # measures taken from graph by a networkx method
        #_allu=["clustering"] # measures taken from an undirected version of the graph by a method of itself
        #_allu_=[] # measures taken from the undirected version of the graph by a networkx method
        self.makeMeasures(network, exclude)
    def makeMeasures(self,network,exclude):
        """Make the network measures"""
        # fazer condicional para cada medida, se não estiver na exclude[],
        # fazer medida de tempo e guardar como tupla no

        g=network.g
        gu=network.gu
        timings=[]

        T=t.time()
        self.N=network.g.number_of_nodes()
        self.E=network.g.number_of_edges()
        self.E_=network.gu.number_of_edges()
        self.edges=     g.edges(data=True)
        self.nodes=     g.nodes(data=True)
        timings.append((t.time()-T,"edges and nodes"))

        T=t.time()
        self.degrees=dict(g.degree())
        self.nodes_= sorted(g.nodes(), key=lambda x : self.degrees[x])
        self.degrees_=[self.degrees[i] for i in self.nodes_]
        self.in_degrees=dict(g.in_degree())
        self.in_degrees_=[self.in_degrees[i] for i in self.nodes_]
        self.out_degrees=dict(g.out_degree())
        self.out_degrees_=[self.out_degrees[i] for i in self.nodes_]
        timings.append((t.time()-T,"in_out_total_degrees"))

        T=t.time()
        self.strengths=     dict(g.degree(weight="weight"))
        self.nodes__= sorted(g.nodes(), key=lambda x : self.strengths[x])
        self.strengths_=[self.strengths[i] for i in self.nodes_]
        self.in_strengths= dict(g.in_degree(weight="weight"))
        self.in_strengths_=[self.in_strengths[i] for i in self.nodes_]
        self.out_strengths=dict(g.out_degree(weight="weight"))
        self.out_strengths_=[self.out_strengths[i] for i in self.nodes_]
        timings.append((t.time()-T,"in_out_total_strengths"))

        # symmetry measures
        self.asymmetries=asymmetries=[]
        self.disequilibrium=disequilibriums=[]
        self.asymmetries_edge_mean=asymmetries_edge_mean=[]
        self.asymmetries_edge_std=asymmetries_edge_std=[]
        self.disequilibrium_edge_mean=disequilibrium_edge_mean=[]
        self.disequilibrium_edge_std=disequilibrium_edge_std=[]
        for node in self.nodes_:
            if not self.degrees[node]:
                asymmetries.append(0.)
                disequilibriums.append( 0.)
                asymmetries_edge_mean.append(0.)
                asymmetries_edge_std .append(0.)    
                disequilibrium_edge_mean.append(0.)
                disequilibrium_edge_std.append(0.)
            else:
                asymmetries.append(
                    (self.in_degrees[node]-self.out_degrees[node])/self.degrees[node])
                disequilibriums.append( 
                    (self.in_strengths[node]-self.out_strengths[node])/self.strengths[node])
                edge_asymmetries=ea=[]
                edge_disequilibriums=ed=[]
                predecessors=g.predecessors(node)
                successors=g.successors(node)
                for pred in predecessors:
                    if pred in successors:
                        ea.append( 0. )
                        ed.append((g[pred][node]['weight']-g[node][pred]['weight'])/self.strengths[node])
                    else:
                        ea.append( 1. )
                        ed.append(g[pred][node]['weight']/self.strengths[node])
                for suc in successors:
                    if suc in predecessors:
                        pass
                    else:
                        ea.append(-1.)
                        ed.append(-g[node][suc]['weight']/self.strengths[node])
                asymmetries_edge_mean.append(   n.mean(ea))
                asymmetries_edge_std .append(   n.std(ea))  
                disequilibrium_edge_mean.append(n.mean(ed))
                disequilibrium_edge_std.append( n.std(ed)) 


        if "weighted_directed_betweenness" not in exclude:
            T=t.time()
            self.weighted_directed_betweenness=x.betweenness_centrality(g,weight="weight")
            self.weighted_directed_betweenness_=[
  self.weighted_directed_betweenness[i] for i in self.nodes_]
            timings.append((t.time()-T,"weighted_directed_betweenness"))
        if "unweighted_directed_betweenness" not in exclude:
            T=t.time()
            self.unweighted_directed_betweenness=x.betweenness_centrality(g)
            timings.append((t.time()-T,"unweighted_directed_betweenness"))
        if "weighted_undirected_betweenness" not in exclude:
            T=t.time()
            self.weighted_undirected_betweenness=x.betweenness_centrality(gu,weight="weight")
            timings.append((t.time()-T,"weighted_undirected_betweenness"))
        if "unweighted_undirected_betweenness" not in exclude:
            T=t.time()
            self.weighted_undirected_betweenness=x.betweenness_centrality(gu)
            timings.append((t.time()-T,"unweighted_undirected_betweenness"))
        if "wiener" not in exclude:
            T=t.time()
            self.wiener=x.wiener_index(g,weight="weight")
            timings.append((t.time()-T,"weiner"))
        if "closeness" not in exclude:
            T=t.time()
            self.closeness=x.vitality.closeness_vitality(g,weight="weight")
            timings.append((t.time()-T,"closeness"))
        if "transitivity" not in exclude:
            T=t.time()
            self.transitivity=x.transitivity(g)
            timings.append((t.time()-T,"transitivity"))
        if "rich_club" not in exclude:
            T=t.time()
            self.rich_club=x.rich_club_coefficient(gu)
            timings.append((t.time()-T,"rich_club"))

        if "weighted_clustering" not in exclude:
            T=t.time()
            self.weighted_clusterings=x.clustering( network.gu ,weight="weight")
            self.weighted_clusterings_=[self.weighted_clusterings[i] for i in self.nodes_]
            timings.append((t.time()-T,"weighted_clustering"))
        if "clustering" not in exclude:
            T=t.time()
            self.clusterings=x.clustering( network.gu )
            self.clusterings_=[self.clusterings[i] for i in self.clusterings]
            timings.append((t.time()-T,"clustering"))
        if "triangles" not in exclude:
            T=t.time()
            self.triangles=x.triangles(gu)
            timings.append((t.time()-T,"clustering"))
        if "n_weakly_connected_components" not in exclude:
            T=t.time()
            self.n_weakly_connected_components=x.number_weakly_connected_components(g)
            timings.append((t.time()-T,"n_weakly_connected_components"))
        if "n_strongly_connected_components" not in exclude:
            T=t.time()
            self.n_strongly_connected_components=x.number_strongly_connected_components(g)
            timings.append((t.time()-T,"n_strongly_connected_components"))
        T=t.time()
        foo=[i for i in x.connected_component_subgraphs(gu)]
        bar=sorted(foo,key=lambda x: x.number_of_nodes(),reverse=True)
        self.component=c=bar[0]
        timings.append((t.time()-T,"component"))
        T=t.time()
        self.diameter=x.diameter(c)
        self.radius=x.radius(c)
        self.center=x.center(c)
        self.periphery=x.periphery(c)
        timings.append((t.time()-T,"radius_diameter_center_periphery"))
        self.timings=timings

        T=t.time()
        self.n_connected_components=x.number_connected_components(gu)
        nodes=[]
        nodes_components=[foo.nodes() for foo in x.connected_component_subgraphs(gu)][:1]
        for nodes_ in nodes_components: nodes+=nodes_
        self.periphery_=nodes
        self.timings=timings









