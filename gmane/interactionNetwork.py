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
        for tid in listStructures.message_ids:
            m=listStructures.messages[tid]
            if m[0] in g.nodes(): # author
                if "weight" in g.node[m[0]].keys():
                    g.node[m[0]]["weight"]+=1
                else:
                    g.add_node(m[0],weight=1.)
                    respondido_antes.append(i)
            else:
                g.add_node(m[0],weight=1.)
            if m[1]:
                if m[1] in mm.keys():
                    m0=mm[m[1]]

                    if g.has_edge(m0[0],m[0]):
                        g[m0[0]][m[0]]["weight"]+=1
                    else:
                        g.add_edge(m0[0], m[0], weight=1.)
                else:
                    resposta_perdida.append(i)

        self.g=g
        self.resposta_perdida=resposta_perdida
        self.respondido_antes=respondido_antes
        # retirando os selfloops, pois o interesse é na interação
        g_=x.copy.deepcopy(g)
        g_.remove_edges_from(g_.selfloop_edges())
        self.g_=g_



