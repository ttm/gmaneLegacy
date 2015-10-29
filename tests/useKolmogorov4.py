import re, time, numpy as n, gmane as g
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
check("começa")

f=open("../extraData/top-output.txt")
aa=f.read()

def Z(a):
    """The z-score"""
    a_=n.array(a)
    return (a_-a_.mean())/a_.std()
def prep(a):
    aa=[float(aaa) for aaa in a]
    return Z(aa)

cpu1=prep( re.findall(r" ([1-9]*.[1-9]*) id, ",aa) )
cpu2=prep( re.findall(r" ([1-9]*.[1-9]*) wa, ",aa) )
cpu3=prep( re.findall(r" ([1-9]*.[1-9]*) us, ",aa) )
mem=prep( re.findall(r"KiB Mem: .* ([1-9]*) used, ",aa) )

proc1=[re.split(r" *",i)[-4:-2] for i in re.findall(r"%CPU .*\n(.*)\n",aa)]
pc,pm=prep([i[0] for i in proc1]),prep([i[1] for i in proc1])

proc2=[re.split(r" *",i)[-4:-2] for i in re.findall(r"%CPU .*\n.*\n(.*)\n",aa)]
pc2,pm2=prep([i[0] for i in proc2]),prep([i[1] for i in proc2])

proc3=[re.split(r" *",i)[-4:-2] for i in re.findall(r"%CPU .*\n.*\n.*\n(.*)\n",aa)]
pc3,pm3=prep([i[0] for i in proc3]),prep([i[1] for i in proc3])

pp_=[cpu1,cpu2,cpu3,mem,pc,pm,pc2,pm2,pc3,pm3]

dists=[]
for i in pp_:
    dists+=[[]]
    for j in pp_:
        dists[-1]+=[g.kolmogorovSmirnovDistance(i,j)]
        check(("j"))
    check(("i"))
fname="osDistances.tex"
caption=r"Values of $c'$ for histograms drawn from laptop system resource status measures."
labels=["cpu1","cpu2","cpu3",
            "mem",
            "p1","m1",
            "p2","m2",
            "p3","m3"]
labelsh=[""]+labels
g.lTable(labels,labelsh,dists,caption,TDIR+fname,"osDistances")

## tabgeral
labelsh=("label","description","events")
data=[ ["workload of the most active processor",
        "workload of the second most active processor",
        "workload of the third most active processor",
        "RAM use in kB",
        "workload use of most consuming process",
        "RAM use of most consuming process",
        "workload use of second most consuming process",
        "RAM use of second most consuming process",
        "RAM use of third most consuming process",
        "workload use of third most consuming process"] ]
events=[len(i) for i in pp_]
data+=[events]
data_=[[i[j] for i in data] for j in range(len(pp_))]
caption="General description of the laptop system status data used for the $c'$ values of the next table. Each event is a measure in a snapshot of system status."
fname="osGeneral.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"osGeneral")



#ff=open("../extraData/top-output.txt")
