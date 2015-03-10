==================================================================
Python utilities for the analysis of the GMANE email list database
==================================================================

This project delivers helper classes for the analysis of the GMANE
email database.

Functionalities are based on physics articles on interaction networks:
- Stability in human interaction networks: primitive typology of vertex, prominence of measures and activity statistics: http://arxiv.org/abs/1310.7769
- A connective differentiation of textual production in interaction networks: http://arxiv.org/abs/1412.7309
- Versinus: a visualization method for graphs in evolution: http://arxiv.org/abs/1412.7311

With core concepts of 1) analysis of topological structure; 2) analysis of textual production; 3) visualization of evolving structures. Activity distribution along time and among participants are also approached through specific routines and indirectly through 1), 2) and 3).

Ideally, this package should ease:
- Downloading GMANE email list data.
- Building elementary data structures with downloaded data.
- Analysis of data through complex networks and NLP criteria.
- Visualization through diverse layout methods.

Usage example
=================
Download messages from one GMANE list:

.. code:: python

    import gmane as g
    dl=g.DownloadGmaneData() # saves into ~/.gmane/
    dl.downloadListsIDS() # acquires all GMANE list_ids
    dl.downloadListMessages(dl.list_ids[100])
    dl.cleanDownloadedLists() # remove empty messages for coherence
    dl.downloadedStats() # creates ~/.gmane/stats.txt

    # to load message contents to Python objects:
    # load 10 messages from list with list_id gmane.ietf.rfc822
    lm=g.LoadMessages("gmane.ietf.rfc822",10)

    # or access the structures downloaded to your filesystem
    dl=g.DownloadGmaneData()
    dl.getDownloadedLists()
    lms=[]
    # and download all messages from 5 lists
    for list_id in dl.downloaded_lists[:5]:
        lms.append(g.LoadMessages(list_id))

    # to load first three lists with the greated number
    # of downloaded messages:
    dl.downloadedStats() # might take a while
    load_msgs=[]
    for list_stat in dl.lists[:3]:
        list_id=list_stat[0]
        load_msgs.append(g.LoadMessages(list_id))

    # to make basic datastructures of a list with
    # greatest number of messages:
    ds=g.MessageDataStructures(load_msgs[0])
    mm=ds.messages
    ids=ds.message_ids
    print("first: ", mm[ids[0]][2], "last:", mm[ids[-1]][2])
    
    # build the interaction network of the messages:
    nw=g.InteractionNetwok(ds)

    print("number of nodes: {}, number of edges: {}".format(
    nw.g.number_of_nodes(), nw.g.number_of_edges()))

    nm=g.NetworkMeasures(nw)

    np=g.NetworkPartitioning(nm)
    sa=np.sectorialized_agents
    print("{} agents in periphery,\
{} are intermediary and {} hubs".format(sa[0],sa[1],sa[2]))

    # Enjoy!
