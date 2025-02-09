from scipy.io import wavfile
from scipy.signal import cwt
import pywt as w, gmane as g, time
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
TDIR_="/usr/share/sounds/alsa/"
fnames=("Front_Center.wav","Front_Left.wav",
        "Rear_Center.wav","Rear_Left.wav",
        "Noise.wav")
def normalize(sig):
    return 2*(sig-sig.min()/(sig.min()-sig.max()))-1
wfiles=[wavfile.read(TDIR_+fname) for fname in fnames]
wfiles_=[normalize(i[1]) for i in wfiles]
wt=[w.wavedec(i,"db8") for i in wfiles_]
#wt_=[]
#for i in range(len(wt)):
#    wt_+=[wt[i][0],wt[i][11]]
#dists=[]
#check("antes")
#for i in wt_:
#    dists+=[[]]
#    for j in wt_:
#        dists[-1]+=[g.kolmogorovSmirnovDistance(i,j)]
#        check(("j",j))
#    check(("i",i))
#dists2=[]
#for w1 in wfiles_:
#    dists2+=[[]]
#    for w2 in wfiles_:
#        dists2[-1]+=[g.kolmogorovSmirnovDistance(w1,w2)]
#        check(("w1",w1))
#    check(("w2",w2))
S=[]
for i in range(len(wt)):
    S+=[wfiles_[i],wt[i][0],wt[i][11]]
dists2=[]
dists3=[]
check("antes")
for i in S:
    dists2+=[[]]
    dists3+=[[]]
    for j in S:
        ksd=g.kolmogorovSmirnovDistance_(i,j)
        dists2[-1]+=[ksd[0]]
        dists3[-1]+=[ksd[2]]
        check(("j"))
    check(("i"))
data_=[(i,j) for i,j in zip(dists2,dists3)]
data__=[i for j in data_ for i in j]
#labels=[[i.format(j) for i in("$S{}$",r"$W_1 {}$","$W_2 {}$")]
#         for j in range(1,6)]
labels=[[i.format(j) for i in("S{}",r"W1-{}","W2-{}")]
         for j in range(1,6)]
labels=[i for j in labels for i in j]
labelsh=[""]+labels
labels_=[(l,"") for l in labels]
labels__=[i for j in labels_ for i in j]
fname="audioDistances.tex"
caption=r"""Values of $c$ for histograms drawn from sound PCM samples and wavelet leaf coefficients.
The different types of the signals yield greater $c$ values."""
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"audioDistances")

labelsh=("label","description","events")
data=[["recorded 'front center'",
      "first wavelet approximation",
      "higher wavelet leaf",
      "recorded 'front left'",
      "first wavelet approximation",
      "higher wavelet leaf",
      "recorded 'rear center'",
      "first wavelet approximation",
      "higher wavelet leaf",
      "recorded 'rear left'",
      "first wavelet approximation",
      "higher wavelet leaf",
      "noise",
      "first wavelet approximation",
      "higher wavelet leaf"]]
events=[len(i) for i in S]
data+=[events]
data_=[[i[j] for i in data] for j in range(len(S))]
caption="""General description of the audio data used for the $c$ values of the next table.
The recorded data events are the PCM samples normalized to fit [-1,1].
The wavelet first approximation consists of the low frequencies.
The higher leaf consists of an approximation of one of the last details."""
fname="audioGeneral.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"audioGeneral")

# fazer com wavelets mais especificas
# : a aproximacao do detalhe da aproximacao da aproximaca, por exemplo
