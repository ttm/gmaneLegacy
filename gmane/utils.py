# função que faz todas as etapas
# de construção da rede
# e entrega os objetos certinho
import gmane as g, time, numpy as n, re, nltk as k, collections as c, string, pickle
from nltk.corpus import wordnet as wn
puncts=set(string.punctuation)
w=open("./wordsEn.txt","r")
w=w.read()
WL=w.split()
WL.append("email")
WL.append("e-mail")
WL_=set(WL)
stopwords=set(k.corpus.stopwords.words("english"))
f=open("pickledir/brill_tagger3","rb")
brill_tagger=pickle.load(f)
f.close()

class EmailStructures:
    """Class that makes all basic structures for a given email list"""
    def __init__(self,list_id,n_messages,text="yes"):
        TT=time.time()
        lid=list_id; TOTAL_M=n_messages
        lm=g.LoadMessages(lid,TOTAL_M,basedir="~/.gmane3/")
        ds=g.ListDataStructures(lm,text="yes")
        print(lid+"{0:.2f} for loading messages and making datastructures".format(time.time()-TT)); TT=time.time()

        print(lid+"{0:.2f} for data structures".format(time.time()-TT)); TT=time.time()
        ts=g.TimeStatistics(ds)
        print("{0:.2f} for statistics along time".format(time.time()-TT)); TT=time.time()
        iN=g.InteractionNetwork(ds)
        nm=g.NetworkMeasures(iN,exclude=["rich_club"])
        print("{0:.2f} for network measures".format(time.time()-TT)); TT=time.time()
        np2_=g.NetworkPartitioning(nm,2,"g")
        del np2_.binomial
        print("{0:.2f} for network partition".format(time.time()-TT)); TT=time.time()
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
def makeText(ds,mid=None):
    if not mid:
        t=[ds.messages[i][3] for i in ds.message_ids]
    else:
        t=[ds.messages[i][3] for i in mid]
    T_="\n".join(t) # todo o texto, com contracoes
    T,ncontractions=REPLACER.replace(T_) # todo o texto, sem contracoes
    return T, ncontractions

def medidasTokens(T):
    atime=time.time()
    wtok=wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=wtok_=[t.lower() for t in wtok]
    nt=len(wtok) #
    ntd=len(set(wtok)) # 
    # tokens que sao pontuacoes
    ntp=sum([sum([tt in puncts for tt in t])==len(t) for t in wtok]) #
    # known and unkown words
    kw=[] #
    ukw=[] #
    tp=[]
    sw=[]
    for t in wtok_:
        if t in WL_:
            kw.append(t)
        elif sum([tt in puncts for tt in t])==len(t):
            tp.append(t)
        else:
            ukw.append(t)
        if t in stopwords:
            sw.append(t)
    sw_=set(sw)
    kw_=set(kw)
    ukw_=set(ukw)
    kwss=[i for i in kw if wn.synsets(i)] #
    kwss_=set(kwss) #
    # known words that does not have synsets
    kwnss=[i for i in kw if i not in kwss_] #
    print("MT2:", atime-time.time()); atime=time.time()
    kwnss_=set(kwnss) #
    # words that are stopwords
    kwsw=[i for i in kw if i in stopwords] #
    kwsw_=set(kwsw)
    print("MT3:", atime-time.time()); atime=time.time()
    # known words that are not stopwords
    kwnsw=[i for i in kw if i not in stopwords] #
    kwnsw_=set(kwnsw) #
    # unknown words that are stopwords
    ukwsw=[i for i in ukw if i in stopwords] #
    print( "MT4:", atime-time.time()); atime=time.time()
    # known words that return synsets and are stopwords
    kwsssw=[i for i in kwss if i in stopwords] #
    print("MT5:", atime-time.time()); atime=time.time()
    # known words that dont return synsets and are stopwords
    kwnsssw=[i for i in kwnss if i in stopwords] #
    print("MT6:", atime-time.time()); atime=time.time()
    # words that are known, are not stopwords and do not return synset
    foo_=kwnss_.difference(stopwords)
    kwnssnsw=[i for i in kw if i in foo_] #
    print("MT7:", atime-time.time()); atime=time.time()
    foo_=kwss_.difference(stopwords) 
    kwssnsw=[i for i in kw if i in foo_] #
    kwssnsw_=set(kwssnsw)
    print("MT8:", atime-time.time()); atime=time.time()
    mvars=("nt", "ntd", "ntp","sw","sw_","kw", "kw_", "tp", "ukw", "ukw_", "kwss", "kwss_", "kwnss", "kwnss_","kwsw", "kwsw_", "kwnsw", "kwnsw_", "ukwsw", "kwsssw", "kwnsssw", "kwnssnsw", "kwssnsw","kwssnsw_")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict

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
    np=sum([t in puncts for t in T])
    # numerais
    nd=sum([t.isdigit() for t in T])
    return nc,ne/nc,nl/(nc-ne),nm/nl,nv/nl,np/(nc-ne),nd/(nc-ne)

def mediaDesvio(tid="astring",adict={"stringkey":"tokens"}):
    tid_=tid+"_"
    toks=[len(i) for i in adict[tid]]
    toks_=[len(i) for i in adict[tid_]]

    mtid=n.mean(toks)
    dtid=n.std(toks)
    mtid_=n.mean(toks_)
    dtid_= n.std(toks_)

    fdict={}
    fdict["m"+tid]=mtid
    fdict["d"+tid]=dtid
    fdict["m"+tid_]=mtid_
    fdict["d"+tid_]=dtid_

    return fdict

def medidasTamanhosTokens(medidas_tokens):
    mdict={}
    MT=medidas_tokens
    mdict.update(mediaDesvio("kw",MT))
    mdict.update(mediaDesvio("kwnsw",MT))
    mdict.update(mediaDesvio("kwssnsw",MT))
    mdict.update(mediaDesvio("kwssnsw",MT))
    mdict.update(mediaDesvio("kwsw",MT))
    mdict.update(mediaDesvio("sw",MT))
    return mdict

def medidasTamanhosSentencas(T,medidas_tokens):
    mdict={}
    MT=medidas_tokens
    ############
    # medidas de sentencas
    TS=k.sent_tokenize(T)
    # media e desvio de numero de caracteres por sentenca
    tTS=[len(i) for i in TS]
    mtTS=n.mean(tTS) #
    dtTS=n.std(tTS) #
    
    # media e desvio do tamanho das sentencas em tokens
    sTS=[k.tokenize.wordpunct_tokenize(i) for i in TS] ### Para os POS tags
    tsTS=[len(i) for i in sTS]
    mtsTS=n.mean(tsTS) #
    dtsTS=n.std(tsTS) #

    # media e desvio do tamanho das sentencas em palavras conhecidas
    kw_=MT["kw_"]
    tsTSkw=[len([ii for ii in i if ii in kw_]) for i in sTS]
    mtsTSkw=n.mean(tsTSkw) #
    dtsTSkw=n.std(tsTSkw) #

    # media e desvio do tamanho das sentencas em palavras que retornam synsets e nao sao stopwords
    pv_=MT["kwssnsw_"]
    tsTSpv=[len([ii for ii in i if ii in pv_]) for i in sTS]
    mtsTSpv=n.mean(tsTSpv) #
    dtsTSpv=n.std(tsTSpv) #

    mvars=("mtTS","dtTS","mtsTS","dtsTS","mtsTSkw","dtsTSkw",
           "mtsTSpv","dtsTSpv","sTS")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def medidasTamanhosMensagens(ds, tids=None):
    if not tids:
        mT=[ds.messages[i][3] for i in ds.message_ids]
    else:
        mT=[ds.messages[i][3] for i in tids]

    tmT=[len(t) for t in mT] # chars
    ttmT=[len(k.tokenize.wordpunct_tokenize(t)) for t in mT] # tokens
    tsmT=[len(k.sent_tokenize(t)) for t in mT] # sentences

    mtmT=n.mean(tmT)
    dtmT=n.std(tmT)
    mttmT=n.mean(ttmT)
    dttmT=n.std(ttmT)
    mtsmT=n.mean(tsmT)
    dtsmT=n.std(tsmT)
    mvars=("mtmT","dtmT","mttmT","dttmT","mtsmT","dtsmT")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def medidasPOS(sentences_tokenized):
    """Measures of POS tags

    Receives a sequence of sentences,
    each as a sequence of tokens.
    Returns a set measures of POS tags,
    and the tagged sentences"""

    tags=brill_tagger.tag_sents(sentences_tokenized)
    tags_=[item for sublist in tags for item in sublist]
    tags__=[i[1] for i in tags_ if i[0].lower() in WL_]
    htags=c.Counter(tags__)

    if htags:
       	factor=100.0/sum(htags.values())
        htags_={}
        for i in htags.keys(): htags_[i]=htags[i]*factor    
        htags__=c.OrderedDict(sorted(htags_.items(), key=lambda x: x[1]))
    mvars=("htags__","tags")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
