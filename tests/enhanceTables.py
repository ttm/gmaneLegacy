# this file is dedicated to
# enhance already finished latex tables.
import gmane as g, importlib, re, os
ENV=os.environ["PATH"]
importlib.reload(g.tableHelpers)
dreload(g,exclude="pytz")
os.environ["PATH"]=ENV

TDIR="/home/r/repos/kolmogorov-smirnov/tables/"
def dl(fname,hl,vl,over=0):
    tablefname=TDIR+fname
    tablefname+=".tex"
    foo=g.doubleLines(tablefname,hlines=hl,vlines=vl)
    if not over:
        tablefname=tablefname.replace(".tex","_.tex")
    g.writeTex(foo,tablefname)
def me(fname,mark,locs,over=1):
    fn=TDIR+fname+".tex"
    foo=g.markEntries_(fn,mark,locs)
    if not over:
        tn=tn.replace(".tex","_.tex")
    g.writeTex(foo,fn)

dl("tabNormNull",[1],[])
dl("tabUniformNull",[1],[])
dl("tabWeibullNull",[1],[])
dl("tabPowerNull",[1],[])

dl("tabNormDiff3",[1],[],)
#g.markEntries_(TDIR+"tabNormDiff3.tex","\\bf",[(1,i) for i in         range(0,12)])
me("tabNormDiff3_","\\bf",[(6,i) for i in         range(0,12)])

dl("tabNormDiffMean",[1],[],)
#g.markEntries_(TDIR+"tabNormDiffMean.tex","\\bf",[(1,i) for i in      range(0,12)])
me("tabNormDiffMean_","\\bf",[(1,i) for i in      range(0,12)])

dl("tabUniformDiffSpread",[1],[],)
me("tabUniformDiffSpread_","\\bf",[(7,i) for i in range(0,12)])

dl("tabUniformDiffMean",[1],[],)
me("tabUniformDiffMean_","\\bf",[(1,i) for i in   range(0,12)])

dl("tabWeibullDiffShape",[1],[],)
me("tabWeibullDiffShape_","\\bf",[(9,i) for i in  range(0,12)])

dl("tabPowerDiffShape",[1],[],)
me("tabPowerDiffShape_","\\bf",[(5,i) for i in    range(0,12)])


dl("textsGeneral",[1],[1],)
me("textsGeneral_","\\bf",[(i,0) for i in range(1,5)])
dl("textsDistances",[1,4,7,10],[1,4,7,10],)
me("textsDistances_","\\bf",[(i,0) for i in range(1,13)])
me("textsDistances_","\\bf",[(0,i) for i in range(1,13)])
dl("textsDistances2",[1,4,7,10],[1,4,7,10],)
me("textsDistances2_","\\bf",[(i,0) for i in range(1,13)])
me("textsDistances2_","\\bf",[(0,i) for i in range(1,13)])
dl("textsDistances2b",[1,4,7,10],[1,4,7,10],)
me("textsDistances2b_","\\bf",[(i,0) for i in range(1,13)])
me("textsDistances2b_","\\bf",[(0,i) for i in range(1,13)])
dl("textsDistances3",[1,4,7,10],[1,4,7,10],)
me("textsDistances3_","\\bf",[(i,0) for i in range(1,13)])
me("textsDistances3_","\\bf",[(0,i) for i in range(1,13)])
dl("textsDistances4",[1,4,7,10],[1,4,7,10],)
me("textsDistances4_","\\bf",[(i,0) for i in range(1,13)])
me("textsDistances4_","\\bf",[(0,i) for i in range(1,13)])
dl("textsDistances4b",[1,4,7,10],[1,4,7,10],)
me("textsDistances4b_","\\bf",[(i,0) for i in range(1,13)])
me("textsDistances4b_","\\bf",[(0,i) for i in range(1,13)])


dl("audioGeneral",[1],[1],)
me("audioGeneral_","\\bf",[(i,0) for i in range(1,16)])

dl("audioDistances",[1,4,7,10,13],[1,4,7,10,13],)
me("audioDistances_","\\bf",[(i,0) for i in range(1,16)])
me("audioDistances_","\\bf",[(0,i) for i in range(1,16)])


dl("musicGeneral",[1],[1],)
me("musicGeneral_","\\bf",[(i,0) for i in range(1,9)])

dl("musicDistances",[2,4,6,8],[2,4,6,8],)
me("musicDistances_","\\bf",[(i,0) for i in range(1,9)])
me("musicDistances_","\\bf",[(0,i) for i in range(1,9)])
g.writeTex(g.fSize(TDIR+"musicDistances_.tex","\\scriptsize"),TDIR+"musicDistances_.tex")


dl("osGeneral",[1],[1],)
me("osGeneral_","\\bf",[(i,0) for i in range(1,11)])

dl("osDistances",[4,5,7,9,11],[4,5,7,9,11],)
me("osDistances_","\\bf",[(i,0) for i in range(1,11)])
me("osDistances_","\\bf",[(0,i) for i in range(1,11)])
g.writeTex(g.fSize(TDIR+"osDistances_.tex","\\scriptsize"),TDIR+"osDistances_.tex")




#tablefname="tabNormDiff3.tex"
#with open(TDIR+tablefname,"r") as f:
#    lines=f.read()
#
#linesB=lines[:]
#
#i=4
#linha=re.findall(r"\\hline\n.*"*i+r"\\hline\n(.*)\\hline\n",lines)[0]
#j=2
#
#elementos=[i.strip() for i in linha.split("&")]
#elementos_=elementos[:]
#elementos_[-1],resto=elementos[-1].split(" ")
#elemento=elementos_[j]
#
##lspl=linha.split(" ")
##elemento=lspl[j*2]
#marcador="\\bf"
#elemento_="{{{} {}}}".format(marcador,elemento)
##lspl[j*2]=elemento_
#elementos_[j]=elemento_
##linha_=" ".join(lspl)
#linha_=" & ".join(elementos_)+" "+resto
#if lines.count(linha)==1:
#    lines_=lines.replace(linha,linha_)
#elif lines.count(linha)>1:
#    print("mais de uma linha igual ERRO!!!")
#else:
#    print("linha não existe!!! ERRO!!")

##g.writeTex(lines_,tablefname)
#
## colocando barras nas linhas verticais
#header=re.findall(r"\\begin{tabular}{(.*)}\\hline\n",lines)[0]
#indexes=[i.start() for i in re.finditer("\|",header)]
#js=1,3
#header_=header[:]
#foo=0
#for j in js:
#    j_=indexes[j]+foo
#    header_=header_[:j_]+"||"+header_[j_+1:]
#    foo+=1
#
#lines__=lines.replace(header,header_)
#
## colocando barras nas linhas horizontais
#linhas=lines.split("\\hline")
#ii=0,1,4
#linesF=lines[:]
#for i in ii:
#    linha=linhas[i]
#    linha_=linha+"\\hline"
#    if lines.count(linha)==1:
#        linesF=linesF.replace(linha,linha_)
#    elif lines.count(linha)>1:
#        print("mais de uma linha igual ERRO!!!")
#    else:
#        print("linha não existe!!! ERRO!!")
#lines___=linesF



