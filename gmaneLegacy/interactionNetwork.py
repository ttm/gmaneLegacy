import networkx as x
class InteractionNetwork:
    """Delivers the interaction network of email data structures

    Network is directed and weighted.

    Usage
    =====
    Initialize with a MessageDataStructures() instance.
    """
    def __init__(self,listStructures=None):
        if not listStructures:
            g.listDataStructures()
        g=x.DiGraph()
        self.makeGraph(listStructures, g)
    def makeGraph(self,listStructures, g):
        """Make the interaction digraph"""
        for tid in listStructures.message_ids:
            m=listStructures.messages[tid]
            if m[0] in g.nodes(): # author
                g.node[m[0]]["weight"]+=1
            else:
                g.add_node(m[0],weight=1.)
            if m[1]:
                if m[1] in listStructures.message_ids:
                    m0=listStructures.messages[m[1]]
                    if g.has_edge(m0[0],m[0]):
                        g[m0[0]][m[0]]["weight"]+=1
                    else:
                        if m0[0] not in g.nodes():
                            g.add_node(m0[0],weight=0.)
                        g.add_edge(m0[0], m[0], weight=1.)
        # no selfloops, as interest is on interaction
        g.remove_edges_from(g.selfloop_edges())
        self.g=g
        self.gu=g.to_undirected()
