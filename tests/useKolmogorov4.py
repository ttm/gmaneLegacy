import re, time, numpy as n, gmane as g
TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
TT=time.time()
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
check("começa")

#f=open("../extraData/top-output.txt")
#aa=f.read()
#f.close()
#
#def Z(a):
#    """The z-score"""
#    a_=n.array(a)
#    return (a_-a_.mean())/a_.std()
#def prep(a):
#    aa=[float(aaa) for aaa in a]
#    return Z(aa)
#
#cpu1=prep( re.findall(r" ([1-9]*.[1-9]*) id, ",aa) )
#check("cpu1")
#cpu2=prep( re.findall(r" ([1-9]*.[1-9]*) wa, ",aa) )
#check("cpu2")
#cpu3=prep( re.findall(r" ([1-9]*.[1-9]*) us, ",aa) )
#check("cpu3")
#mem=prep( re.findall(r"KiB Mem: .* ([1-9]*) used, ",aa) )
#check("cpu4")
#
#proc1=[re.split(r" *",i)[-4:-2] for i in re.findall(r"%CPU .*\n(.*)\n",aa)]
#pc,pm=prep([i[0] for i in proc1]),prep([i[1] for i in proc1])
#check("proc")
#
#proc2=[re.split(r" *",i)[-4:-2] for i in re.findall(r"%CPU .*\n.*\n(.*)\n",aa)]
#pc2,pm2=prep([i[0] for i in proc2]),prep([i[1] for i in proc2])
#check("proc")
#
#proc3=[re.split(r" *",i)[-4:-2] for i in re.findall(r"%CPU .*\n.*\n.*\n(.*)\n",aa)]
#pc3,pm3=prep([i[0] for i in proc3]),prep([i[1] for i in proc3])
#check("proc")
import pickle
#pp_=[cpu1,cpu2,cpu3,mem,pc,pm,pc2,pm2,pc3,pm3]
#fn="../extraData/os.pickle"
#f=open(fn,"wb")
#pickle.dump(pp_,f)
#f.close()

fn="../extraData/os.pickle"
f=open(fn,"rb")
pp_=pickle.load(f)
f.close()


dists=[]
dists2=[]
for i in pp_:
    dists+=[[]]
    dists2+=[[]]
    for j in pp_:
        ksd=g.kolmogorovSmirnovDistance_(i,j)
        dists[-1]+=[ksd[0]]
        dists2[-1]+=[ksd[2]]
        check(("j"))
    check(("i"))
data_=[(i,j) for i,j in zip(dists,dists2)]
data__=[i for j in data_ for i in j]
check("kolm")
fname="osDistances.tex"
caption=r"Values of $c$ for histograms drawn from laptop system resource status measures."
labels=["cpu1","cpu2","cpu3",
            "mem",
            "p1","m1",
            "p2","m2",
            "p3","m3"]
labelsh=[""]+labels
labels_=[(l,"") for l in labels]
labels__=[i for j in labels_ for i in j]
g.lTable(labels__,labelsh,data__,caption,TDIR+fname,"osDistances")

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
caption="General description of the laptop system status data used for the $c$ values of the next table. Each event is a measure in a snapshot of system status."
fname="osGeneral.tex"
g.lTable(labels,labelsh,data_,caption,TDIR+fname,"osGeneral")



#ff=open("../extraData/top-output.txt")
