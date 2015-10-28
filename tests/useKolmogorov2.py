from scipy.io import wavfile
from scipy.signal import cwt
import pywt as w, gmane as g, time
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()


TDIR_="/usr/share/sounds/alsa/"
fnames=("Front_Center.wav","Front_Left.wav",
        "Rear_Center.wav","Rear_Left.wav","Noise.wav")
def normalize(sig):
    return sig-sig.min()/(sig.min()-sig.max())-0.5
wfiles=[wavfile.read(TDIR_+fname) for fname in fnames]
wfiles_=[normalize(i[1]) for i in wfiles]
wt=[w.dwt(i,"db8") for i in wfiles_]
wt_=[]
for i in range(len(wt)):
    wt_+=[wt[i][0],wt[i][1]]
dists=[]
check("antes")
for i in wt_:
    dists+=[[]]
    for j in wt_:
        dists[-1]+=[g.kolmogorovSmirnovDistance(i,j)]
        check(("j",j))
    check(("i",i))
dists2=[]
for w1 in wfiles_:
    dists2+=[[]]
    for w2 in wfiles_:
        dists2[-1]+=[g.kolmogorovSmirnovDistance(w1,w2)]
        check(("w1",w1))
    check(("w2",w2))

# fazer com wavelets mais especificas
# : a aproximacao do detalhe da aproximacao da aproximaca, por exemplo
