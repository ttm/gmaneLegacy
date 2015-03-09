import networkx as x, time as t
class NetworkMeasures:
    """Extracts measures for incoming network.

    Both overall measures and measures of each vertex are taken.
    """
    def __init__(self,network=None,exclude=["unweghted_undirected_betweenness","weighted_undirected_betweenness","unweighted_directed_betweenness"]):
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
        timings=[]
        if "weighted_directed_betweenness" not in exclude:
            T=t.time()
            g=network.g
            gu=network.gu
            self.weighted_directed_betweenness=x.betweenness_centrality(g,weight="weight")
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
        if "weiner" not in exclude:
            T=t.time()
            self.weiner=x.vitality.weiner_index(g,weight="weight")
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
            self.weighted_clustering=x.clustering( network.gu ,weight="weight")
            timings.append((t.time()-T,"weighted_clustering"))
        if "clustering" not in exclude:
            T=t.time()
            self.clustering=x.clustering( network.gu )
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

        T=t.time()
        self.degree=g.degree()
        self.in_degree=g.in_degree()
        self.out_degree=g.out_degree()
        timings.append((t.time()-T,"in_out_total_degrees"))

        T=t.time()
        self.strength=     g.degree(weight="weight")
        self.in_strength= g.in_degree(weight="weight")
        self.out_strength=g.out_degree(weight="weight")
        timings.append((t.time()-T,"in_out_total_strengths"))
        self.timings=timings


