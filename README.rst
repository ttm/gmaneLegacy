==================================================================
Python utilities for the analysis of the GMANE email list database
==================================================================

This project delivers helper classes for the analysis of the GMANE
email database. Install with:

    $ pip install gmaneLegacy

or

    $ python setup.py install

For greater control of customization (and debugging), clone the repo and install with pip with -e:

    $ git clone https://github.com/ttm/gmaneLegacy.git

    $ pip install -e <path_to_repo>

This install method is especially useful with
reload function from IPython.lib.deepreload and the standard importlib.

Functionalities are based on physics articles on interaction networks:
[1] Stability in human interaction networks: primitive typology of vertex, prominence of measures and activity statistics: http://arxiv.org/abs/1310.7769
[2] A connective differentiation of textual production in interaction networks: http://arxiv.org/abs/1412.7309
[3] Versinus: a visualization method for graphs in evolution: http://arxiv.org/abs/1412.7311

With core concepts of 1) analysis of topological structure; 2) analysis of textual production; 3) visualization of evolving structures. Activity distribution along time and among participants are also approached through specific routines and indirectly through 1), 2) and 3).

Ideally, this package should ease:
- Downloading GMANE email list data.
- Building elementary data structures with downloaded data.
- Analysis of data through complex networks and NLP criteria.
- Visualization through diverse layout methods.

PS.
Implemented measures of symmetry in network agents activity by hand (not found in network and numeric packages) according to [1].
PS2.
ongoing research in 
tests/newTextTables.py and
tests/makeOverallTextAnalysis.py
PS.
Also check the gmane Python package https://github.com/ttm/gmane


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

    # circular (directional) statistics for activity along time
    # (hours of the day, days of the week, days of the month, etc):
    # mean_vec, mean_angle, size_mean_vec, circular_mean,
    # circular_variance, circular dispersion
    # and histograms
    ts=g.TimeStatistics(ds)
    print("made overall circular activity statistics along time")

    # make latex tables to observe distributions within bins of interest
    hi=100*ts.hours["histogram"]/ts.hours["histogram"].sum()
    row_labels=list(range(24))
    tstring=g.parcialSums(row_labels,data=[hi],partials=[1,2,3,4,6,12],
                partial_labels=["h","2h","3h","4h","6h","12h"],datarow_labels=["APACHE"])
    g.writeTex(tstring,"here.tex")

    ps=g.AgentStatistics(ds)
    print("made overall activity statistics among participants")
    
    # build the interaction network of the messages:
    nw=g.InteractionNetwok(ds)

    print("number of nodes: {}, number of edges: {}".format(
    nw.g.number_of_nodes(), nw.g.number_of_edges()))

    nm=g.NetworkMeasures(nw) # take measures, including symmetry related measures
    np=g.NetworkPartitioning(nm) # partition in primitive typology
    sa=np.sectorialized_agents # get members of each sector
    print("{} agents in periphery, {} are intermediary and {} hubs".format(sa[0],sa[1],sa[2]))
    sa=np.sectorialized_agents__ # smoothed histogram for classification
    print("{} agents in periphery, {} are intermediary and {} hubs".format(sa[0],sa[1],sa[2]))

    # draw
    nd=g.NetworkDrawer()
    print("drawer started")
    nd.makeLayout(nm)
    print("gave (x,y) for each author with 5-15-80")
    nd2=g.NetworkDrawer()
    print("drawer two started")
    nd2.makeLayout(nm,np)
    print("gave (x,y) for each author with \
    sectors by comparison with Erdos-Renyi")
    nd.drawNetwork( iN,nm ,"test.png")
    nd2.drawNetwork( iN,nm,"test2.png")

    # make basic PCA plots of network measures:
    npca=g.NetworkPCA(nm)
    # Plot PCA with a colored primitive sectors 
    npca=g.NetworkPCA(nm,np)

    # Evolves network with measures, partitions,
    # PCA, principal components and Versinus plots saved to disk
    lm=lms[0] # loaded messages from list with most messages
    ne=g.NetworkEvolution(step_size=10)
    ne.evolveRaw(lm.messages,imagerate=4,erdos_sectors=True)
    # ne.makeVideo() use this to avoid evolving again just to make video
    # see testDrawer.py or g.NetworkEvolution to make movies:
    # https://www.youtube.com/watch?v=iS8NwEy291g

    # after making network evolution measurements and video,
    # you can both make music:
    em=g.EvolutionMusic()
    print("music is done")
    # avconv -i mixY.wav -i evo[..<depends on the evolution done>..].avi final.avi
    # delivers you the final.avi animation with a soundtrack relative to network measures
    # currently it is the 'four hubs dance' by default:
    # https://www.youtube.com/watch?v=YxDiwzAUPeU

    # and further analysis of measures and Erdos sectors:
    et=g.EvolutionTimelines()
    print("Written png files with network measures along evolution timeline")

    # Enjoy!

Further documentation is in tests/ folder and object docstrings.
