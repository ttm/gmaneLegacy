import numpy as n, string
def markEntries(table,marker):
    """Make entries in a table boldface or use other markings"""
    # open rendered table as text
    print("YEAH")
    with open(table,"r") as f:
        lines=f.read()
    lines=lines.split("\n")
    lines[3:-3]=[i.split("&") for i in lines[3:-3]]
    for i,line in enumerate(lines[3:-3]):
        i1,i2=line[-1].split("\\\\\\")
        i2="\\\\\\"+i2
        lines[i+3]=line[:-1]+[i1,i2]
    print(lines)
    print(len(lines[0]))
    for column in range(1,len(lines[3])-1):
        print("column")
        values=[]
        for linei in range(3,len(lines)-3):
            if lines[linei][column].strip(): # can be empty
                value=float(lines[linei][column].split("{")[-1].split("}")[0])
                values.append(value)
        print(values)
        mav=max(values)
        miv=min(values)
        print(mav,miv)
        for linei in range(3,len(lines)-3):
            if lines[linei][column].strip(): # can be empty
                orig="{:.2f}".format(mav)
                tnew="\\{}{{ {} }}".format(marker,mav)
                print(orig,tnew)
                lines[linei][column]=lines[linei][column].replace(orig,tnew)
    lines=lines[:3]+[" & ".join(line[:-1])+line[-1] for line in lines[3:-3]]+lines[-3:]
    lines=" \n ".join(lines)
    writeTex(lines,table.replace(".tex","_.tex"))
    # find maximum and minimum in each row
    # boldface them all
    return lines
def makeTables(labels,data,two_decimal=False):
    """Returns a latex table of data with Label in first column.
    
    Returns latex printable or writable to files to
    be imported by latex files.
    """
    if len(labels)!=len(data):
        print("input one label per data row")
        return
    if not two_decimal:
        data="".join([(labels[i]+" & {} "*len(datarow)+"\\\\\\hline\n").format(*datarow) for i, datarow in enumerate(data)])
    else:
        print("BBBBBBBBBBBB",labels)
        if labels[0]=="$cc$" and len(labels)>10:
            print("AAAAAAAAAAA",labels)
            data="".join([((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) if labels[i] in ("$cc$","$bt$") else (((labels[i]+" & %.2f "*len(datarow)+"\\\\\n")%tuple(datarow)) if labels[i] != "$\\sigma_{dis}$" else ((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\\hline\n")%tuple(datarow))) for i, datarow in enumerate(data)])
        elif type(data[0][0])==type("astring"):
            #data="".join([((labels[i]+" & %s "+" & %.2f "*(len(datarow)-1)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
            data="".join([((labels[i]+" & %s "+" & %.2f "*(len(datarow)-1)+"\\\\\\hline\n")%tuple(datarow)) if type(datarow[0])==type("astring") else ((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data) ])
        else:
            data="".join([((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
    return data

def partialSums(labels, data, partials,partial_labels="",datarow_labels=""):
    """Returns a latex table with sums of data.

    Data is though to be unidimensional. Each row
    is transposed to a column to which partial sum
    are added.
    """

    lines=[]
    for label in labels:
        lines.append("{} ".format(label))
    for datarow in data:
        for partial in partials:
            for line_num in range(len(datarow)):
                if (line_num%partial)==0:
                    lines[line_num]+="& \\multirow{{{:d}}}{{*}}{{ {:.2f} }}  ".format(partial,sum(datarow[line_num:line_num+partial]))
                else:
                    lines[line_num]+="& "

    for line_num in range(len(lines)):
        cuts=[(0==(line_num+1)%partial) for partial in partials]
        i=0
        suffix=""
        for cut in cuts:
            if cut:
                for datarownum in range(len(data)):
                    num=i+(datarownum)*len(partials)
                    suffix+="\\cline{{{}-{}}}".format(num+2,num+2)
            i+=1
        lines[line_num]+="\\\\{}\n".format(suffix)
    
    ltable="".join(lines)

    if partial_labels:
        header=( (" & {}"*len(partial_labels)).format(*partial_labels) )*len(data)+" \\\\\\hline\n"
        ltable=header+ltable
    if datarow_labels:
        header=((" & \\multicolumn{{%i}}{{c|}}{{{}}}"%(len(partials),))*len(datarow_labels)).format(*datarow_labels)+" \\\\\\hline\n"
        ltable=header+ltable
    header="\\begin{center}\n\\begin{tabular}{| l ||"+" c |"*len(data)*len(partials)+"}\\hline\n"
    footer="\\hline\\end{tabular}\n\\end{center}"
    ltable=header+ltable+footer
    return ltable

def pcaTable(labels,vec_mean,vec_std,val_mean,val_std):
    """Make table with PCA formation mean and std"""

    header="\\begin{center}\n\\begin{tabular}{| l |"+" c |"*6+"}\\cline{2-7}\n"
    header+="\\multicolumn{1}{c|}{} & \\multicolumn{2}{c|}{PC1}          & \multicolumn{2}{c|}{PC2} & \multicolumn{2}{c|}{PC3}  \\\\\\cline{2-7}"
    header+="\\multicolumn{1}{c|}{} & $\mu$            & $\sigma$ & $\mu$         & $\sigma$ & $\mu$ & $\sigma$  \\\\\\hline\n"
    tt=n.zeros((vec_mean.shape[0],6))
    tt[:,::2]=vec_mean
    tt[:,1::2]=vec_std
    tt_=n.zeros(6)
    tt_[::2]=val_mean
    tt_[1::2]=val_std
    tab_data=n.vstack((tt,tt_))
    footer="\\hline\\end{tabular}\n\\end{center}"
    table=header + makeTables(labels,tab_data,True) + footer
    return table

def writeTex(string,filename):
    with open(filename,"w") as f:
        f.write(string)
