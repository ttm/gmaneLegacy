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
def min3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[:3]]
def max3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[-3:]]

class KSStatistics:
    """Hold references and simulation routines"""
    alfas=[0.1,0.05,0.025,0.01,0.005,0.001]
    calfas=[1.22,1.36,1.48,1.63,1.73,1.95]
    def __init__(self,,NC,NE,NB,adir="/home/r/repos/kolmogorov-smirnov/",NE2=0):
        table_dir=adir+"tables/"
        aux_dir=adir+"aux/"
        if not NE2:
            NE2=NE
        # self.makeAll(NC,NE,NB,aux_dir,table_dir)
    def makeAll(self,NC,NE,NE2,NB,aux_dir,table_dir):
        makePreambule(NC,NE,NE2,NB,aux_dir):
        makeNormalVerification(NC,NE,NE2,NB,table_dir)
        makeUniformVerification(NC,NE,NE2,NB,table_dir)
        makeWeibullVerification(NC,NE,NE2,NB,table_dir)
        makePowerVerification(NC,NE,NE2,NB,table_dir)

    def makePreambule(self,NC,NE,NE2,NB,aux_dir):
        fname=aux_dir+"preambule1.tex"
        preambule=r"""The number of comparisons is $N_c={}$,
        each with the sample sizes of $n={}$ and $n'={}$.
        Each histogram have $N_b={}$ equally spaced bins.""".format(
                NC,NE,NE2,NB)
        with f=open(,"w"):
            f.write(preambule)
    def makeNormalVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[g.kolmogorovSmirnovDistance(
                n.random.normal(0,1,NE),n.random.normal(0,1,NE2))
                for i in range(NC)]; check("normal1")
        dists2=[g.kolmogorovSmirnovDistance(
                n.random.normal(3,2,NE),n.random.normal(3,2,NE2))
                for i in range(NC)]; check("normal2")
        dists3=[g.kolmogorovSmirnovDistance(
                n.random.normal(6,3,NE),n.random.normal(6,3,NE2))
                for i in range(NC)]; check("normal3")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for significance levels $\alpha$.
        The $c_1$ values were calculated using simulations of normal distributions with $\mu={}$ and $\sigma={}$.
        The $c_2$ values were calculated using simulations of normal distributions with $\mu={}$ and $\sigma={}$.
        The $c_3$ values were calculated using simulations of normal distributions with $\mu={}$ and $\sigma={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
        """.format(        0,1,
                3,2,
                6,3,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   )
        data=[]
        labels=[]
        for alfa, calfa in zip(alfas,calfas):
            n1=sum([dist>calfa for dist in dists])
            n2=sum([dist>calfa for dist in dists2])
            n3=sum([dist>calfa for dist in dists3])
            data.append((alfa,calfa,n1,n2,n3))
            labels.append(alfa*ND)
        fname="tabNormNull.tex"
        g.lTable(labels,labelsh,data,caption,table_dir+fname)
        print("table {} written at {}".format(fname,table_dir))
    def makeUniformVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[g.kolmogorovSmirnovDistance(
                n.random.random(NE),n.random.random(NE2))
                for i in range(NC)]; check("uniforme1")
        dists2=[g.kolmogorovSmirnovDistance(
                2*n.random.random(NE)+2,2*n.random.random(NE2)+2)
                for i in range(NC)]; check("uniforme2")

        dists3=[g.kolmogorovSmirnovDistance(
                3*n.random.random(NE)+4,3*n.random.random(NE2)+4)
                for i in range(NC)]; check("uniforme3")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for critical values of $\alpha$.
        The $c_1$ values were calculated using simulations of uniform distributions within $[{},{})$.
        The $c_2$ values were calculated using simulations of uniform distributions within $[{},{})$.
        The $c_3$ values were calculated using simulations of uniform distributions with $\mu={}$ and $\sigma={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
        """.format(
                0,1,
                2,6,
                4,10,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   )
        data=[]
        labels=[]
        for alfa, calfa in zip(alfas,calfas):
            n1=sum([dist>calfa for dist in dists])
            n2=sum([dist>calfa for dist in dists2])
            n3=sum([dist>calfa for dist in dists3])
            data.append((alfa,calfa,n1,n2,n3))
            labels.append(alfa*ND)
            print(n1, alfa*ND )
            print(sum([dist>calfa for dist in dists2]), alfa*ND )
            print(sum([dist>calfa for dist in dists3]), alfa*ND )
        fname="tabUniformNull.tex"
        g.lTable(labels,labelsh,data,caption,table_dir+fname)
        print("table {} written at {}".format(fname,table_dir))
    def makeWeibullVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[g.kolmogorovSmirnovDistance(
                n.random.weibull(0.1,NE),n.random.weibull(0.1,NE2))
                for i in range(NC)]; check("weibull1")
        dists2=[g.kolmogorovSmirnovDistance(
                n.random.weibull(2,NE),n.random.weibull(2,NE2))
                for i in range(NC)]; check("weibull2")
        dists3=[g.kolmogorovSmirnovDistance(
                n.random.weibull(4,NE),n.random.weibull(4,NE2))
                for i in range(NC)]; check("weibull3")
        dists4=[g.kolmogorovSmirnovDistance(
                n.random.weibull(6,NE),n.random.weibull(6,NE2))
                for i in range(NC)]; check("weibull4")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$",r"$|C_4(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for critical values of $\alpha$.
        The $c_1$ values were calculated using simulations of 1-parameter Weibull distributions with $a={}$.
        The $c_2$ values were calculated using simulations of 1-parameter Weibull distributions with $a={}$.
        The $c_3$ values were calculated using simulations of 1-parameter Weibull distributions with $a={}$.
        Over all $N_c$ comparisons,
        The $N_o$ values of $c_4$ were calculated using simulations of
         1-parameter Weibull distributions with $a={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
         $\mu(c_4)={:.4f}$ and $\sigma(c_4)={:.4f}$ .
        """.format(
                0.1,
                2,
                4,
                6,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   n.mean(dists4),n.std(dists4),
                   )
        data=[]
        labels=[]
        for alfa, calfa in zip(alfas,calfas):
            n1=sum([dist>calfa for dist in dists])
            n2=sum([dist>calfa for dist in dists2])
            n3=sum([dist>calfa for dist in dists3])
            n4=sum([dist>calfa for dist in dists4])
            data.append((alfa,calfa,n1,n2,n3,n4))
            labels.append(alfa*ND)
            print(n1, alfa*ND )
            print(sum([dist>calfa for dist in dists2]), alfa*ND )
            print(sum([dist>calfa for dist in dists3]), alfa*ND )
        fname="tabWeibullNull.tex"
        g.lTable(labels,labelsh,data,caption,table_dir+fname)
        print("table {} written at {}".format(fname,table_dir))
    def makePowerVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[g.kolmogorovSmirnovDistance(
                n.random.power(0.3,NE),n.random.power(0.3,NE2))
                for i in range(NC)]; check("power1")
        dists2=[g.kolmogorovSmirnovDistance(
                n.random.power(1,NE),n.random.power(1,NE2))
                for i in range(NC)]; check("power2")
        dists3=[g.kolmogorovSmirnovDistance(
                n.random.power(2,NE),n.random.power(2,NE2))
                for i in range(NC)]; check("power3")
        dists4=[g.kolmogorovSmirnovDistance(
                n.random.power(3,NE),n.random.power(3,NE2))
                for i in range(NC)]; check("power4")
        dists4_=[g.kolmogorovSmirnovDistance(
                n.random.power(4,NE),n.random.power(4,NE2))
                for i in range(NC)]; check("power5")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$",r"$|C_4(\alpha)|$",r"$|C_5(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for critical values of $\alpha$.
        The $c_1$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_2$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_3$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_4$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_5$ values were calculated using simulations of power functions distributions with $a={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
         $\mu(c_4)={:.4f}$ and $\sigma(c_4)={:.4f}$ .
         $\mu(c_5)={:.4f}$ and $\sigma(c_5)={:.4f}$ .
        """.format(
                0.3,
                1,
                2,
                3,
                4,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   n.mean(dists4),n.std(dists4),
                   n.mean(dists4_),n.std(dists4_),
                   )
        data=[]
        labels=[]
        for alfa, calfa in zip(alfas,calfas):
            n1=sum([dist>calfa for dist in dists])
            n2=sum([dist>calfa for dist in dists2])
            n3=sum([dist>calfa for dist in dists3])
            n4=sum([dist>calfa for dist in dists4])
            n4_=sum([dist>calfa for dist in dists4_])
            data.append((alfa,calfa,n1,n2,n3,n4,n4_))
            labels.append(alfa*ND)
        fname="tabPowerNull.tex"
        g.lTable(labels,labelsh,data,caption,TDIR+fname)
        print("table {} written at {}".format(fname,table_dir))




