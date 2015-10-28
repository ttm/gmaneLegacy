from music21 import *
import gmane as g, time
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
check("começa")
palestrina= corpus.parse("palestrina/Sanctus_69.krn")
pitchesp=[i.midi for i in palestrina.pitches]
check("palestrina")

#bach_ = corpus.parse('bach/bwv73.5')
#pitches_=[i.midi for i in bach.pitches]

bach0 = corpus.parse('bach/bwv73.5.mxl')
pitches0=[i.midi for i in bach0.pitches]
bach = corpus.parse('bach/bwv64.8.mxl')
pitches=[i.midi for i in bach.pitches]
check("bach")
#bach2 = corpus.parse('bach/bwv84.5')
#pitches2=[i.midi for i in bach.pitches]

# mozart
mozart0 = corpus.parse('mozart/k80/movement3.mxl')
pitchesm0=[i.midi for i in mozart0.pitches]
mozart = corpus.parse('k458/movement1.mxl')
pitchesm=[i.midi for i in mozart.pitches]
check("mozart")

# beethoven
beet0= corpus.parse("beethoven/opus18no1/movement3.krn")
pitchesb0=[i.midi for i in beet0.pitches]
beet= corpus.parse("beethoven/opus132.mxl")
pitchesb=[i.midi for i in beet.pitches]
check("beethoven")

# shoenberg
shoen= corpus.parse('schoenberg/opus19/movement2.mxl')
pitchess=[i.midi for i in shoen.pitches]
check("shoenberg")

# z-score de todo mundo
# bate nas distancias de kolmogorov-smirnov
# coloca duração se quiser
pp=[pitchesp,
        pitches0,pitches,
        pitchesm0,pitchesm,
        pitchesb0,pitchesb,
        pitchess,
        ]
dists=[]
for i in pp:
    dists+=[[]]
    for j in pp:
        dists[-1]+=[g.kolmogorovSmirnovDistance(i,j)]
        check(("j",j))
    check(("i",i))
fname="musicDistances.tex"
caption=r"Values of $c'$ for histograms drawn from the pitches of classical compositions."
labels=["Pale",
            "Bach1","Bach2",
            "Moza1","Moza2",
            "Beet1","Beet2",
            "Shoe"]
labelsh=[""]+labels
g.lTable(labels,labelsh,dists,caption,TDIR+fname,"musicDistances")

## tabgeral
labelsh=("label","description","events")
data=[["Sanctus 69 from G. P. da Palestrina",
        "BWV735 from J. S. Bach",
        "BWV648 from J. S. Bach",
        "K80 from W. A. Mozart",
        "K458 from W. A. Mozart",
        "Opus 18, n1, mov. 3 from L. van Beethoven",
        "Opus 132 from L. van Beethoven",
        r"Opus 19, mov. 2 from A. Sh\"nberg"]]
events=[len(i) for i in pp]
data+=[events]
data_=[[i[j] for i in data] for j in range(len(pp))]
caption="General description of the music data used for the $c'$ values of the next table. Each event is a midi value of a note pitch."
fname="musicGeneral.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"audioGeneral")





