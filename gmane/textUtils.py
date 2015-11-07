# função que faz todas as etapas
# de construção da rede
# e entrega os objetos certinho
import gmane as g, time, numpy as n, re, nltk as k, collections as c, string, pickle
from nltk.corpus import wordnet as wn
puncts=set(string.punctuation)
#w=open("./wordsEn.txt","r")
#w=w.read()
#WL=w.split()
WL2=k.corpus.words.words()
#w=open("./wordlist.txt","r")
w=open("./words.txt","r")
# https://raw.githubusercontent.com/dwyl/english-words/master/words.txt
w=w.read()
WL=w.split()

#WL.append("email")
#WL.append("e-mail")
#WL.append("having")
WL_=set(WL)
WLP=k.corpus.floresta.words()
WLP_=set(WLP)
stopwords=set(k.corpus.stopwords.words("english"))
stopwordsP=set(k.corpus.stopwords.words("portuguese"))
f=open("pickledir/brill_taggerT2M1","rb")
brill_tagger=pickle.load(f)
f.close()
DL=g.tableHelpers.dl
ME=g.tableHelpers.me

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
def perc_(alist):
    if type(alist) in (type([1,2]), type((2,4))):
        return [100*i/sum(alist[1:]) for i in alist]
    else:
        return 100*alist/alist[1:].sum()
def perc(alist):
    if type(alist) in (type([1,2]), type((2,4))):
        return [100*i/sum(alist) for i in alist]
    else:
        return 100*alist/alist.sum()
def digRoot(msgid,ds):
    layers=[[msgid]]
    while len(layers[-1]):
        layer=layers[-1]
        layers+=[[]]
        for mid in layer:
            if mid in ds.responses.keys():
                layers[-1]+=[i[0] for i in ds.responses[mid]]
    return layers,len(layers)

def generalMeasures(ds,np,ts):
    """Return overall measures from list datastructures and network partitioning"""
    #date1=ds.messages[ds.message_ids[0]][2].isoformat().split("T")[0]
    #date2=ds.messages[ds.message_ids[-1]][2].isoformat().split("T")[0]
    dt=ts.datetimes
    primeira,ultima=dt[0],dt[-1]
    date1=primeira.isoformat()[:-6]
    date2=ultima.isoformat(  )[:-6]
    deltaAnos=(ultima-primeira)
    deltaAnos_=deltaAnos.days/365.2425

    N=ds.n_authors
    Ns=[len(i) for i in np.sectorialized_agents__]
    Ns_=perc(Ns)
    M_=ds.n_messages-ds.n_empty
    M=ds.n_messages
    #Mh=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[2]])
    #Mi=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[1]])
    #Mp=sum([len(ds.author_messages[author]) for author in np.sectorialized_agents__[0]])
    #Ms=[Mh,Mi,Mp][::-1]
    Ms=[sum([len(ds.author_messages[i]) for i in j])
        for j in np.sectorialized_agents__]
    #M2=[100*i/ds.n_messages for i in Ms]
    Ms_=perc(Ms)
    NM=N/M
    NM_=100*NM
    NM_missing=M_/N
    NM_missing_=100*NM_missing
    NMs=[i/j if j!=0 else n.inf for i,j in zip(Ns,Ms)]
    NMs_=perc(NMs)
    #idsh=[i[0] for j in np.sectorialized_agents__[2] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    #idsi=[i[0] for j in np.sectorialized_agents__[1] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    #idsp=[i[0] for j in np.sectorialized_agents__[0] for i in ds.author_messages[j] if ds.messages[i[0]][1]==None]
    #idsh_=len(idsh)
    #idsi_=len(idsi)
    #idsp_=len(idsp)
    #ids=[idsh_,idsi_,idsp_][::-1]
    #ids_=[100*ii/Gamma for ii in ids]
    #Gamma=len([i for i in ds.message_ids if ds.messages[i][1]==None])
    Gammas=[sum([len([i for i in ds.author_messages[aid] if i[1]==None])
           for aid in sa]) for sa in np.sectorialized_agents__]
    Gammas_=perc(Gammas)
    G_=[100*i/j for i,j in zip(Gammas,Ms)]
    # Gammas_==ids_
    #roots=[[[i for i in ds.author_messages[aid] if i[1]==None]
    #           for aid in sa] for sa in pr.sectorialized_agents__]
    #roots_=[i for j in roots for i in j]
    ## *) a partir de cada uma delas, procura outras que tenham
    ## ela como resposta e assim por diante,
    ## até não achar mais resposta, guarda o número de mensagens
    ## encontradas
    #roots__=[[[i[j][0] for j in range(len(i))] for i in rr if i] for rr in roots]
    #rr=[]
    roots_sectors=[]
    tlength_sectors=[]
    threads_sectors=[]
    for setor in np.sectorialized_agents__:
        roots_sector=[]
        tlength_sector=[]
        threads_sector=[]
        for agentid in setor:
            messages=ds.author_messages[agentid]
            for message in messages:
                if message[1]==None: # nova thread, guarda ID
                    roots_sector.append(message[0])
                    t_sector,lsector=digRoot(message[0],ds)
                    tlength_sector.append(lsector)
                    threads_sector.append(t_sector)
        roots_sectors.append(roots_sector)
        tlength_sectors.append(tlength_sector)
        threads_sectors.append(threads_sector)
    mt=[n.mean(i) for i in tlength_sectors]
    st=[n.std(i) for i in tlength_sectors]
    tls=[i for j in tlength_sectors for i in j]
    mt_ =n.mean(tls)
    st_ =n.std(tls)
    mvars=("date1","date2","deltaAnos_",
            "N","Ns","Ns_","M","M_","Ms","Ms_",
            "NM","NM_","NMs","NMs_","NM_missing","NM_missing_",
            "Gammas","Gammas_","G_",
            "roots_sectors","tlength_sectors","threads_sectors",
            "mt","st","tls","mt_","st_")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
    #return date1,date2,N,Ns,Ns_,Ms,M2,Gamma,ids,ids_,M_,MN,MN_
def makeGeneralTable(generalMeasures_instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="geralInline.tex"):
    gms=generalMeasures_instance
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$N$",r"$N_{\%}$",r"$M$",r"$M_{\%}$",
            r"$\Gamma$",r"$\Gamma_{\%}$",r"$\frac{\Gamma}{M}\%$",
            r"$\mu(\gamma)$",r"$\sigma(\gamma)$")
    N,Ns,Ns_,M,Ms,Ms_,Gammas,Gammas_,G_,mt_,mt,st_,st,deltaAnos_,date1,date2=[gms[i]
            for i in ("N","Ns","Ns_","M","Ms","Ms_","Gammas","Gammas_","G_","mt_","mt","st_","st","deltaAnos_","date1","date2")]
    Gamma=sum(Gammas)
    data=[[N]+Ns,[100]+Ns_,[M]+Ms,[100]+Ms_,[Gamma]+Gammas,[100]+Gammas_,[100*Gamma/M]+G_,[mt_]+mt,[st_]+st]
    caption=r"""Distribution of participants, messages and threads among each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, 
    {{\bf h.}} for hubs) in a total time period of {:.2f} years (from {} to {}). $N$ is the number of participants, $M$ is the number of messages, $\Gamma$ is the number of threads, and $\gamma$ is the number of messages in a thread.
    The \% denotes the usual `per cent' with respecto to the total quantity ($100\%$ for {{\bf g.}})
    while $\mu$ and $\sigma$ denote mean and standard deviation.""".format(deltaAnos_,date1,date2)
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral")
    dl=g.tableHelpers.dl
    me=g.tableHelpers.me
    me(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    dl(table_dir+fname[:-4]+"_",[1],[1],list(range(2,8,2))+[8,9])



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
def makeText_(ds,pr):
    texts=[]
    msg_ids=[]
    textG=""
    for sector in pr.sectorialized_agents__:
        texts+=[""]
        msg_ids.append([])
        for author in sector:
            for message in ds.author_messages[author]:
                mid=message[0]
                text=ds.messages[mid][3]
                texts[-1]+=text
                textG+=text
                msg_ids[-1].append(mid)
    texts=[textG]+texts
    foo=[REPLACER.replace(i) for i in texts]
    texts_=[i[0] for i in foo]
    ncontractions=[i[1] for i in foo]
    return texts_,ncontractions, msg_ids
def makeText(ds,mid=None):
    if not mid:
        t=[ds.messages[i][3] for i in ds.message_ids]
    else:
        t=[ds.messages[i][3] for i in mid]
    T_="\n".join(t) # todo o texto, com contracoes
    T,ncontractions=REPLACER.replace(T_) # todo o texto, sem contracoes
    return T, ncontractions

def medidasTokensQ_(T,lang="en"):
    atime=time.time()
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
    if lang=="en":
        kw=[len(i) for i in wtok_ if i in WL_]
        sw=[len(i) for i in wtok_ if i in stopwords]
    else:
        kw=[len(i) for i in wtok_ if i in WLP_]
        sw=[len(i) for i in wtok_ if i in stopwordsP]
    mvars=("kw","sw")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def medidasTokensQ(T,lang="en"):
    atime=time.time()
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
    if lang=="en":
        kw=[len(i) for i in wtok_ if i in WL_]
        sw=[len(i) for i in wtok_ if i in stopwords]
    else:
        kw=[len(i) for i in wtok_ if i in WLP_]
        sw=[len(i) for i in wtok_ if i in stopwordsP]
    mkw=n.mean(kw)
    dkw=n.std(kw)
    msw=n.mean(sw)
    dsw=n.std(sw)
    mvars=("mkw","dkw","msw","dsw")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def makeSentencesTable(medidasSentencas_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="sentencesInline.tex"):
    sms=medidasSentencas_dict
    mvars=("nsents",
            "Mchars_sents","Schars_sents",
            "Mtoks_sents","Stoks_sents",
            "Mknownw_sents","Sknownw_sents",
            "Mstopw_sents","Sstopw_sents",
            "Mpuncts_sents","Spuncts_sents",)
    sms_=[[sms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$sents$",r"$sents_{\%}$",
            r"$\mu_S(chars)$", r"$\sigma_S(chars)$",
            r"$\mu_S(tokens)$",r"$\sigma_S(tokens)$",
            r"$\mu_S(knownw)$",r"$\sigma_S(knownw)$",
            r"$\mu_S(stopw)$", r"$\sigma_S(stopw)$",
            r"$\mu_S(puncts)$",r"$\sigma_S(puncts)$",
            )
    caption=r"""Sentences sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=sms_
    nsents=data[0]
    nsents_=perc_(nsents)
    data=n.array(data[1:])
    data=n.vstack((nsents,nsents_,data))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,6,8,10,12])

def makeTokenSizesTable(medidasTokens__instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="tokenSizesInline.tex"):
    tms=medidasTokens__instance
    mvars=("Mtoken","Stoken","Mknownw","Sknownw",
            "Mknownw_diff","Sknownw_diff",
            "Mstopw","Sstopw")
    tms_=[[tms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=( r"$\mu(\overline{tokens})$",r"$\sigma(\overline{tokens})$",
            r"$\mu(\overline{knownw})$",r"$\sigma(\overline{knownw})$",
            r"$\mu(\overline{knownw \neq})$",r"$\sigma(\overline{knownw \neq})$",
            r"$\mu(\overline{stopw})$",r"$\sigma(\overline{stopw})$")
    caption=r"""Token sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=tms_
    #ntoks=data[0]
    #ntoks_=perc_(ntoks)
    #data=n.array(data[1:])
    #data=n.vstack((ntoks,ntoks_,data*100))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral_")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,6,8])


def makeTokensTable(medidasTokens__instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="tokensInline.tex"):
    tms=medidasTokens__instance
    mvars=("tokens",
            "tokens_diff",
            "knownw",
            "knownw_diff",
            "stopw",
            "punct",
            "contract")
    tms_=[[tms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$tokens$",
            r"$tokens_{\%}$",
            r"$tokens \neq$",
            r"$\frac{knownw}{tokens}$",
            r"$\frac{knownw \neq}{knownw}$",
            r"$\frac{stopw}{knownw}$",
            r"$\frac{punct}{tokens}$",
            r"$\frac{contrac}{tokens}$",
            )
    caption=r"""tokens in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, 
    {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=tms_
    ntoks=data[0]
    ntoks_=perc_(ntoks)
    data=n.array(data[1:])
    data=n.vstack((ntoks,ntoks_,data*100))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,3,5,7,8])

def medidasTokens__(lt=("texts",),ct=("ncontractions",)):
    return [medidasTokens_(i,j) for i,j in zip(lt,ct)]
def medidasTokens_(T,ncontract):
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
    tokens=len(wtok) #
    tokens_=set(wtok)
    tokens_diff=len(tokens_)/tokens # 
    punct=sum([sum([tt in puncts for tt in t])==len(t) for t in wtok_])
    punct/=tokens
    known=[i for i in wtok_ if (i not in stopwords) and (i in WL_)]
    knownw=len(known)
    known_=set(known)
    knownw_diff=len(known_)/knownw
    stop=[i for i in wtok_ if i in stopwords]
    stopw=len(stop)/knownw
    knownw/=tokens
    contract=ncontract/tokens

    # media e desvio de tamanhos:
    # tokens,
    Mtoken,Stoken=mediaDesvio_(wtok_)
    # known words sem stop,
    Mknownw,Sknownw=mediaDesvio_(known)
    # known words sem stop e sem repetição
    Mknownw_diff,Sknownw_diff=mediaDesvio_(known_)
    # stop words
    Mstopw,Sstopw=mediaDesvio_(stop)

    #stokwn=[len(i) for i in known]
    #skownw=[len(i) for i in known]
    mvars=("tokens","tokens_diff","punct",
            "knownw","knownw_diff","stopw","contract",
            "Mtoken","Stoken","Mknownw","Sknownw",
            "Mknownw_diff","Sknownw_diff",
            "Mstopw","Sstopw")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict

def medidasTokens(T):
    atime=time.time()
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
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

def makeCharTable(charsMeasures_instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="charsInline.tex"):
    cms=charsMeasures_instance
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$chars$",
            r"$chars_{\%}$",
            r"$\frac{spaces}{chars}$",
            r"$\frac{punct}{chars-spaces}$",
            r"$\frac{digits}{chars-spaces}$",
            r"$\frac{letters}{chars-spaces}$",
            r"$\frac{vogals}{letters}$",
            r"$\frac{uppercase}{letters}$",
            )

    caption=r"""Characters in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, 
    {{\bf h.}} for hubs)."""
    data=list(map(list, zip(*cms)))
    nchars=data[0]
    nchars_=perc_(nchars)
    data=n.array(data[1:])
    data=n.vstack((nchars,nchars_,data*100))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,5,7,8])
def medidasLetras_(LT=["list","of","strings"]):
        return [medidasLetras(i) for i in LT]
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
    return nc,ne/nc,np/(nc-ne),nd/(nc-ne),nl/(nc-ne),nv/nl,nm/nl

def mediaDesvio_(medidas):
    medidas_=[len(i) for i in medidas]
    return n.mean(medidas_),n.std(medidas_)
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
def makeMessagesTable(medidasMensagens_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="messagesInline.tex"):
    mms=medidasMensagens_dict
    mvars=("nmsgs",
            "Msents_msgs","Ssents_msgs",
            "Mtokens_msgs","Stokens_msgs",
            "Mknownw_msgs","Sknownw_msgs",
            "Mstopw_msgs","Sstopw_msgs",
            "Mpuncts_msgs","Spuncts_msgs",
            "Mchars_msgs","Schars_msgs",
            )
    mms_=[[mms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$msgs$",r"$msgs_{\%}$",
            r"$\mu_M(sents)$", r"$\sigma_M(sents)$",
            r"$\mu_M(tokens)$",r"$\sigma_M(tokens)$",
            r"$\mu_M(knownw)$",r"$\sigma_M(knownw)$",
            r"$\mu_M(stopw)$", r"$\sigma_M(stopw)$",
            r"$\mu_M(puncts)$",r"$\sigma_M(puncts)$",
            r"$\mu_M(chars)$", r"$\sigma_M(chars)$",
            )

    caption=r"""Messages sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=mms_
    nmsgs=data[0]
    nmsgs_=perc_(nmsgs)
    data=n.array(data[1:])
    data=n.vstack((nmsgs,nmsgs_,data))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,6,8,10,12,14,16])


def medidasMensagens_(ds,msg_ids):
    return [medidasMensagens(ds,mids) for mids in [None]+list(msg_ids)]
def medidasMensagens(ds,tids=None):
    # TTM
    if not tids:
        mT=[ds.messages[i][3] for i in ds.message_ids]
    else:
        mT=[ds.messages[i][3] for i in tids]
    tokens_msgs=[k.tokenize.wordpunct_tokenize(t) for t in mT] # tokens
    knownw_msgs=[[i for i in toks if (i not in stopwords) and (i in WL_)] for toks in tokens_msgs]
    stopw_msgs=[[i for i in toks if i in stopwords] for toks in tokens_msgs]
    puncts_msgs=[[i for i in toks if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for toks in tokens_msgs] #
    sents_msgs=[k.sent_tokenize(t) for t in mT] # tokens
    nmsgs=len(mT)
    Mchars_msgs,   Schars_msgs  = mediaDesvio_(mT)
    Mtokens_msgs,  Stokens_msgs = mediaDesvio_(tokens_msgs)
    Mknownw_msgs,  Sknownw_msgs = mediaDesvio_(knownw_msgs)
    Mstopw_msgs,   Sstopw_msgs  = mediaDesvio_(stopw_msgs)
    Mpuncts_msgs,  Spuncts_msgs = mediaDesvio_(puncts_msgs)
    Msents_msgs,Ssents_msgs     = mediaDesvio_(sents_msgs)
    mvars=("nmsgs",
            "Msents_msgs","Ssents_msgs",
            "Mtokens_msgs","Stokens_msgs",
            "Mknownw_msgs","Sknownw_msgs",
            "Mstopw_msgs","Sstopw_msgs",
            "Mpuncts_msgs","Spuncts_msgs",
            "Mchars_msgs","Schars_msgs",
            )
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def medidasSentencas_(Ts=['list',"of","strings"]):
    return [medidasSentencas(i) for i in Ts]
def medidasSentencas(T):
    TS=k.sent_tokenize(T)
    tokens_sentences=[k.tokenize.wordpunct_tokenize(i) for i in TS] ### Para os POS tags
    knownw_sentences=[[i for i in ts if (i not in stopwords) and (i in WL_)] for ts in tokens_sentences]
    stopw_sentences =[[i for i in ts if i in stopwords] for ts in tokens_sentences]
    puncts_sentences=[[i for i in ts if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for ts in tokens_sentences] #
    Mchars_sents,  Schars_sents  = mediaDesvio_(TS)
    Mtoks_sents,   Stoks_sents   = mediaDesvio_(tokens_sentences)
    Mknownw_sents, Sknownw_sents = mediaDesvio_(knownw_sentences)
    Mstopw_sents,  Sstopw_sents  = mediaDesvio_(stopw_sentences)
    Mpuncts_sents, Spuncts_sents = mediaDesvio_(puncts_sentences)
    nsents=len(TS)
    mvars=("Mchars_sents","Schars_sents",
            "Mtoks_sents","Stoks_sents",
            "Mknownw_sents","Sknownw_sents",
            "Mstopw_sents","Sstopw_sents",
            "Mpuncts_sents","Spuncts_sents","nsents",
            "tokens_sentences")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict



def medidasTamanhosSentencas(T,medidas_tokens):
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
def medidasPOS_(list_of_list_of_sentences_tokenized):
    # [i["tokens_sentences"] for i in sent_measures]
    return [medidasPOS(i) for i in list_of_list_of_sentences_tokenized]
def medidasPOS(sentences_tokenized):
    """Measures of POS tags

    Receives a sequence of sentences,
    each as a sequence of tokens.
    Returns a set measures of POS tags,
    and the tagged sentences.

    Convention:
    VERB - verbs (all tenses and modes)
    NOUN - nouns (common and proper)
    PRON - pronouns 
    ADJ - adjectives
    ADV - adverbs
    ADP - adpositions (prepositions and postpositions)
    CONJ - conjunctions
    DET - determiners
    NUM - cardinal numbers
    PRT - particles or other function words
    X - other: foreign words, typos, abbreviations
    . - punctuation
    
    See "A Universal Part-of-Speech Tagset"
    by Slav Petrov, Dipanjan Das and Ryan McDonald
    for more details:
        http://arxiv.org/abs/1104.2086"""

    tags=brill_tagger.tag_sents(sentences_tokenized)
    tags_=[item for sublist in tags for item in sublist]
    tags__=[i[1] for i in tags_ if i[0].lower() in WL_]
    htags=c.Counter(tags__)

    if htags:
       	factor=100.0/sum(htags.values())
        htags_={}
        for i in htags.keys(): htags_[i]=htags[i]*factor    
        htags__=c.OrderedDict(sorted(htags_.items(), key=lambda x: -x[1]))
    mvars=("htags__","tags")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict

def makePOSTable(posMensagens_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="posInline.tex"):
    pms=posMensagens_dict
#    pms_=[list(i["htags__"].items()) for i in pms]
    #mvars=[list(i["htags__"].keys()) for i in pms]
    #mvars=list(pms[0]["htags__"].keys())
    mvars=['NOUN', 'X', 'ADP', 'DET', 'VERB', 'ADJ', 'ADV', 'PRT', 'PRON', 'NUM', 'CONJ',"."]
    pms__=[[pms[j]["htags__"][i] if (i in pms[j]["htags__"].keys()) else 0 for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=mvars[:-1]+["PUNC"]
    caption=r"""POS tags in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs).
    Universal POS tags~\cite{{petrov}}:
    VERB - verbs (all tenses and modes);
    NOUN - nouns (common and proper);
    PRON - pronouns;
    ADJ - adjectives;
    ADV - adverbs;
    ADP - adpositions (prepositions and postpositions);
    CONJ - conjunctions;
    DET - determiners;
    NUM - cardinal numbers;
    PRT - particles or other function words;
    X - other: foreign words, typos, abbreviations;
    PUNCT - punctuation.
"""
    #data=list(map(list, zip(*tms_)))
    data=pms__
    #nmsgs=data[0]
    #nmsgs_=perc_(nmsgs)
    #data=n.array(data[1:])
    #data=n.vstack((nmsgs,nmsgs_,data))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral_")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,7,9,10,11,12])


def makeMessagesTable(medidasMensagens_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="messagesInline.tex"):
    mms=medidasMensagens_dict
    mvars=("nmsgs",
            "Msents_msgs","Ssents_msgs",
            "Mtokens_msgs","Stokens_msgs",
            "Mknownw_msgs","Sknownw_msgs",
            "Mstopw_msgs","Sstopw_msgs",
            "Mpuncts_msgs","Spuncts_msgs",
            "Mchars_msgs","Schars_msgs",
            )
    mms_=[[mms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$msgs$",r"$msgs_{\%}$",
            r"$\mu_M(sents)$", r"$\sigma_M(sents)$",
            r"$\mu_M(tokens)$",r"$\sigma_M(tokens)$",
            r"$\mu_M(knownw)$",r"$\sigma_M(knownw)$",
            r"$\mu_M(stopw)$", r"$\sigma_M(stopw)$",
            r"$\mu_M(puncts)$",r"$\sigma_M(puncts)$",
            r"$\mu_M(chars)$", r"$\sigma_M(chars)$",
            )

    caption=r"""Messages sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=mms_
    nmsgs=data[0]
    nmsgs_=perc_(nmsgs)
    data=n.array(data[1:])
    data=n.vstack((nmsgs,nmsgs_,data))
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,6,8,10,12,14])



def filtro(wt_):
    # faz separação dos tokens para analise com wordnet
    sword_sem_synset=[]
    sword_com_synset=[]
    word_com_synset=[]
    word_sem_synset=[]
    pontuacao=[]
    token_exotico=[]
    for wt in wt_:
        ss=wn.synsets(wt[0])
        if ss:
            if wt[0] in stopwords:
                sword_com_synset.append(wt)
            else:
                word_com_synset.append((wt[0],wt[1],ss))
        #elif wt[0] in puncts:
        elif sum([tt in puncts for tt in wt[0]])==len(wt[0]):
            pontuacao.append(wt)
        elif wt[0] in stopwords:
            sword_sem_synset.append(wt)
        elif wt[0] in WL_:
            word_sem_synset.append(wt)
        else:
            token_exotico.append(wt)
    mvars=("sword_sem_synset","sword_com_synset","word_com_synset","word_sem_synset","pontuacao","token_exotico")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def traduzPOS(astring):
    if astring in ("NOUN","NNS","NN","NUM"):
        return wn.NOUN
    elif astring in ("VERB","VBG"):
        return wn.VERB
    elif astring in ("ADJ","JJ","ADP"):
        return wn.ADJ+wn.ADJ_SAT
    elif astring in ("ADV","RB","PRT"):
        return wn.ADV
    else:
        return "NOPOS"
        
def medidasWordnet(words_with_pos_tags):
    WT=words_with_pos_tags
    WT_=[(i[0].lower(),i[1]) for j in WT for i in j]
    wlists=filtro(WT_)
    wl=wlists["word_com_synset"]
    posok=[]
    posnok=[]
    for ww in wl:
        pos = traduzPOS(ww[1])
        ss=ww[2]
        # procura nos nomes dos synsets o pos e numeracao mais baixa
        poss=[i.pos() for i in ss]
        fposs=[pp in pos for pp in poss]
        if sum(fposs):
            tindex=fposs.index(True)
            posok.append((ww[0],ss[tindex]))
        else:
            posnok.append(ww)
    # estatísticas sobre posok
    # quais as tags?
    posok_=[i[1].pos() for i in posok]
    ftags=[posok_.count(i)/len(posok) for i in ('s', 'a', 'n', 'r', 'v')]
    mvars=("WT_","wlists","posok","posnok","ftags")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def medidasWordnet2(wndict):
    sss=wndict["posok"]
    sss_=[i[1] for i in sss]
    hyperpaths=[i.hypernym_paths() for i in sss_]
    top_hypernyms=[i[0][:4] for i in hyperpaths]
    lexnames=[i.lexname().split(".")[-1] for i in sss_]

    mhol=[len(i.member_holonyms()) for i in sss_]
    phol=[len(i.part_holonyms()) for i in sss_]
    shol=[len(i.substance_holonyms()) for i in sss_]
    hol=[mhol[i]+phol[i]+shol[i] for i in range(len(sss_))]

    mmer=[len(i.member_meronyms()) for i in sss_]
    pmer=[len(i.part_meronyms()) for i in sss_]
    smer=[len(i.substance_meronyms()) for i in sss_]
    mer=[mmer[i]+pmer[i]+smer[i] for i in range(len(sss_))]

    nlemmas=[len(i.lemmas()) for i in sss_]
    nhyperpaths=[len(i) for i in hyperpaths]
    shyperpaths=[len(i) for j in hyperpaths for i in j]
    nihypernyms=[len(i.instance_hypernyms()) for i in sss_]
    nentailments=[len(i.entailments()) for i in sss_]
    nhypo=[len(i.hyponyms()) for i in sss_]
    nhiypo=[len(i.instance_hyponyms()) for i in sss_]
    maxd=[i.max_depth() for i in sss_]
    mind=[i.min_depth() for i in sss_]
    nregion_domains=[len(i.region_domains()) for i in sss_]
    ntopic_domains= [len(i.topic_domains())  for i in sss_]
    nusage_domains= [len(i.usage_domains())  for i in sss_]
    nsimilar=[    len(i.similar_tos()) for i in sss_]
    nverb_groups=[len(i.verb_groups()) for i in sss_]
    mvars=list(locals().keys()); mvars.remove("wndict")
    mvars_=mvars[:]
    mvars_.remove("sss_");       mvars_.remove("sss");
    mvars_.remove("top_hypernyms")
    mvars_.remove("hyperpaths"); mvars_.remove("lexnames")
    vdict={}
    #mvars=("nmero_part",)
    locals_=locals()
    for mvar in mvars:
        if mvar not in mvars_:
            vdict[mvar] = locals_[mvar]
        else:
            vdict["m"+mvar]=n.mean(locals_[mvar])
            vdict["d"+mvar]=n.std(locals_[mvar])
    return vdict
from sklearn.feature_extraction.text import TfidfVectorizer
def tfIdf(texts):
    """Returns distance matrix for the texts"""
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform([tt.lower() for tt in texts])
    aa=(tfidf * tfidf.T).A
    return aa
def kolmogorovSmirnovDistance(seq1,seq2,bins=300):
    """Calculate distance between histograms
    
    Adapted from the Kolmogorov-Smirnov test"""
    amin=min(min(seq1),min(seq2))
    amax=max(max(seq1),max(seq2))
    bins=n.linspace(amin,amax,bins+1,endpoint=True)
    h1=n.histogram(seq1,bins,density=True)[0]
    h2=n.histogram(seq2,bins,density=True)[0]
    space=bins[1]-bins[0]
    cs1=n.cumsum(h1*space)
    cs2=n.cumsum(h2*space)

    dc=n.abs(cs1-cs2)
    Dnn=max(dc)
    n1=len(seq1)
    n2=len(seq2)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha=Dnn/fact
    return calpha
