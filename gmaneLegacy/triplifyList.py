#import time, os, shutil, datetime, re, random, string
#
#import nltk as k
#import rdflib as r
#
#from urllib.parse import quote
#import percolation as P

import datetime, os, shutil
import percolation as P, gmaneLegacy as G
import html.parser
parser=html.parser.HTMLParser()
U=parser.unescape
c=P.check

def makeRepo(list_data_struct,fpath,fname,comment,aname=None,created_at=None,scriptpath=None,umbrella_dir=None):
    if not created_at:
        created_at=datetime.datetime.now()
    if not aname:
        aname=fname.split("/")[-1].replace(".","-").replace("+","P")
    fname_=fname.split("/")[-1]
    PREFIX="https://raw.githubusercontent.com/OpenLinkedSocialData/{}master/".format(umbrella_dir)
    tg=P.rdf.makeBasicGraph([["po","gmane"],[P.rdf.ns.po,P.rdf.ns.gmane]],"Email messages linked data")
    nchars=0
    for mid in list_data_struct.message_ids:
        message=list_data_struct.messages[mid]
        imsg=P.rdf.IC([tg],P.rdf.ns.gmane.Message,"{}".format(G.utils.urifyID(mid)))
#        if imsg == "http://purl.org/socialparticipation/gmane/Message#200406231741.i5NHfZbO019592_-AT-_sirius.codesourcery.com":
#            print("AQUIII")
        uris=[P.rdf.ns.gmane.mid,P.rdf.ns.gmane.sentAt,P.rdf.ns.gmane.body,P.rdf.ns.gmane.uid]
        tbody=U(message[3])
        nchars+=len(tbody)
        data=[U(mid),message[2],tbody,message[0]]
#        P.utils.breakMe()
        P.rdf.link([tg],imsg,mid,uris,data,draw=False)

        #ind=P.rdf.IC([tg],P.rdf.ns.gmane.Participant,"{}---{}".format(aname,message[0].replace("@","--AT--").replace(">","").replace("<","")))
#        uris=[P.rdf.ns.gmane.author]
#        data=[message[0]]
#        P.rdf.link([tg],ind,message[0],uris,data,draw=False)

        ind=P.rdf.IC([tg],P.rdf.ns.gmane.Participant,"{}".format(G.utils.urifyID(message[0])))
        uris=[P.rdf.ns.gmane.author]
        uris2=[ind]
        if message[1]:
            uris +=[P.rdf.ns.gmane.responseTo]
            imsg2=P.rdf.IC([tg],P.rdf.ns.gmane.Message,"{}".format(G.utils.urifyID(message[1])))
            uris2+=[imsg2]
        P.rdf.link_([tg],imsg,mid,uris,uris2,draw=False)
    tg2=P.rdf.makeBasicGraph([["po","gmane"],[P.rdf.ns.po,P.rdf.ns.gmane]],"Metadata for the snapshot of email messages")
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))
    # escrever tb:
#    P.utils.breakMe()
    nmsgs=list_data_struct.n_messages
    nresponses=sum([i[1]!=None for i in list_data_struct.messages.values()])
    nusers=list_data_struct.n_authors
    # nchars
#    repourl="https://github.com/OpenLinkedSocialData/{}".format(aname)
    repourl="https://github.com/OpenLinkedSocialData/{}tree/master/{}".format(umbrella_dir,aname)
    metaurl="{}rdf/{}Meta.owl".format(PREFIX,aname)
    P.rdf.link([tg2],ind,"Snapshot {}".format(aname),
                          [P.rdf.ns.po.createdAt,
                          P.rdf.ns.po.triplifiedIn,
                          P.rdf.ns.po.donatedBy,
                          P.rdf.ns.po.availableAt,
#                          P.rdf.ns.po.originalFile,
                          P.rdf.ns.po.rdfFile,
                          P.rdf.ns.po.ttlFile,
                          P.rdf.ns.po.discorveryRDFFile,
                          P.rdf.ns.po.discoveryTTLFile,
                          P.rdf.ns.po.acquiredThrough,
                          P.rdf.ns.rdfs.comment,
                          P.rdf.ns.gmane.gmaneID,
                          P.rdf.ns.gmane.nParticipants,
                          P.rdf.ns.gmane.nMessages,
                          P.rdf.ns.gmane.nResponses,
                          P.rdf.ns.gmane.nCharacters,
                          ],
                          [created_at,
                           datetime.datetime.now(),
                           "Gmane database and public list participants",
                           repourl,
#                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname.split("/")[-1]),
                           "{}rdf/{}Translate.owl".format(PREFIX,aname),
                           "{}rdf/{}Translate.ttl".format(PREFIX,aname),
                                metaurl,
                                "{}rdf/{}Meta.ttl".format(PREFIX,aname),
                           "Gmane public database of email lists",
                                comment,
                               fname_,
                               nusers,
                               nmsgs,
                               nresponses,
                               nchars
                           ])
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}{}/".format(fpath,aname)
    c("before write")
    P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1,sizelimit=100000)

    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    shutil.copy(scriptpath,fpath_+"scripts/")
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
#    shutil.copy("{}/*".format(fname),fpath_+"base/")
    c("before zip")
    #P.utils.zipDir2(fname,fpath_+"base/msgs")
    c("before second write")
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,False)

    # faz um README
    dates=[i for i in tg_[0].query(r"SELECT ?p WHERE {?s gmane:sentAt ?p} ORDER BY ASC(?p)")]
    #return tg_
    date1=dates[0][0].value
    date2=dates[-1][0].value
    #return tg_
    #nicks=queryMe(tg_[0],"SELECT ?s ?o WHERE {?s irc:nick ?o}")

    c("before queries")
    #nnicks=P.utils.countMe( tg_[0], "gmane:author")
    #nicks= P.utils.getAll2(  tg_[0],"gmane:author")
    #nicks_=[i.split("@")[-1] for i in nicks]

    #nreplies= P.utils.countMe(tg_[0],   "gmane:responseTo")
    #nmsgs=    P.utils.countMe(  tg_[0], "gmane:body")
    # nchars
    c("before queries")
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from
the email list with id {} in the Gmane public database.
Collected around {}, the {} messages, 
of which {} are replies with a total of {} chars,
concerning {} participants, span from {} to {}.
The linked data is available at rdf/ and was
generated by the routine in the script/ directory.
Metadata for discovery is in file:
{}
All files should be available at the git repository:
{}
\n""".format(
            fname_,created_at,
            nmsgs,nresponses,nchars,nusers,
            date1,date2,
            repourl,metaurl
            ))
    return tg_


