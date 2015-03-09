import networkx as x
class NetworkMeasures:
    """Extracts measures for incoming network.

    Both overall measures and measures of each vertex are taken.
    """
    def __init__(self,network=None,exclude=[]):
        if not network:
            network=g.InteractionNetwork()
        #_all=["clustering"] # measures taken from graph by a method of itself
        #_all_=[] # measures taken from graph by a networkx method
        #_allu=["clustering"] # measures taken from an undirected version of the graph by a method of itself
        #_allu_=[] # measures taken from the undirected version of the graph by a networkx method

        # fazer condicional para cada medida, se não estiver na exclude[],
        # fazer medida de tempo e guardar como tupla no
        timmings=[]
