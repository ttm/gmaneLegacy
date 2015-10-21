# função que faz todas as etapas
# de construção da rede
# e entrega os objetos certinho
import gmane as g, time as T, numpy as n, re
class EmailStructures:
    """Class that makes all basic structures for a given email list"""
    def __init__(self,list_id,n_messages,text="yes"):
        TT=T.time()
        lid=list_id; TOTAL_M=n_messages
        lm=g.LoadMessages(lid,TOTAL_M,basedir="~/.gmane3/")
        ds=g.ListDataStructures(lm,text="yes")
        print(lid+"{0:.2f} for loading messages and making datastructures".format(T.time()-TT)); TT=T.time()

        print(lid+"{0:.2f} for data structures".format(T.time()-TT)); TT=T.time()
        ts=g.TimeStatistics(ds)
        print("{0:.2f} for statistics along time".format(T.time()-TT)); TT=T.time()
        iN=g.InteractionNetwork(ds)
        nm=g.NetworkMeasures(iN,exclude=["rich_club"])
        print("{0:.2f} for network measures".format(T.time()-TT)); TT=T.time()
        np2_=g.NetworkPartitioning(nm,2,"g")
        del np2_.binomial
        print("{0:.2f} for network partition".format(T.time()-TT)); TT=T.time()
        self.structs=lm, ds, ts, iN, nm, np2_
def generalMeasures(ds,np):
    """Return overall measures from list datastructures and network partitioning"""
    date1=ds.messages[ds.message_ids[0]][2].isoformat().split("T")[0]
    date2=ds.messages[ds.message_ids[-1]][2].isoformat().split("T")[0]
    N=ds.n_authors
    Ns=[len(i) for i in np.sectorialized_agents__]
    Ns_=[100*len(i)/N for i in np.sectorialized_agents__]
    M_=ds.n_messages-ds.n_empty
    Mh=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[2]])
    Mi=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[1]])
    Mp=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[0]])
    M=[Mh,Mi,Mp][::-1]
    M2=[100*i/ds.n_messages for i in M]
    MN=M_/N
    MN_=[i/j if j!=0 else n.inf for i,j in zip(M,Ns)]
    idsh=[i[0] for j in np.sectorialized_agents__[2] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    idsi=[i[0] for j in np.sectorialized_agents__[1] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    idsp=[i[0] for j in np.sectorialized_agents__[0] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    idsh_=len(idsh)
    idsi_=len(idsi)
    idsp_=len(idsp)
    ids=[idsh_,idsi_,idsp_][::-1]
    Gamma=len([i for i in ds.message_ids if ds.messages[i][1]==None])
    ids_=[100*ii/Gamma for ii in ids]
    return date1,date2,N,Ns,Ns_,M,M2,Gamma,ids,ids_,M_,MN,MN_
replacement_patterns = [
(r'won\'t', 'will not'),
(r'can\'t', 'can not'),
(r'i\'m', 'i am'),
(r'ain\'t', 'is not'),
(r'(\w+)\'ll', '\g<1> will'),
(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)\'ve', '\g<1> have'),
(r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\'d', '\g<1> would')
]
class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        count_=0
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
            count_+=count
        return s, count_
REPLACER=RegexpReplacer()
import string
def makeText(ds,mid=None):
    if not mid:
        t=[ds.messages[i][3] for i in ds.message_ids]
    else:
        t=[ds.messages[i][3] for i in mid]
    T_="\n".join(t) # todo o texto, com contracoes
    T,ncontractions=REPLACER.replace(T_) # todo o texto, sem contracoes
    return T,t, ncontractions

def medidasLetras(T):
    # quantos caracteres
    nc=len(T)
    # espacos
    ne=T.count(" ")
    # letras (e maiusculas)
    nl=sum([t.isalpha() for t in T])
    nm=sum([t.isupper() for t in T])
    # vogais
    nv=sum([t in ("a","e","i","o","u") for t in T])
    # pontuacao
    np=sum([t in string.punctuation for t in T])
    # numerais
    nd=sum([t.isdigit() for t in T])

    return nc,ne/nc,nl/(nc-ne),nm/nl,nv/nl,np/(nc-ne),nd/(nc-ne)


