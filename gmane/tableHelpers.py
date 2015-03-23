def makeTables(labels,data,filename=None):
    """Returns a latex table of data with Label in first column.
    
    Returns latex printable or writable to files to
    be imported by latex files.
    """
    if len(labels)!=len(data):
        print("input one label per data row")
        return
    data="".join([(labels[i]+" & {} "*len(datarow)+"\\\\\\hline\n").format(*datarow) for i, datarow in enumerate(data)])
    return data

def parcialSums(labels, data, partials,partial_labels="",datarow_labels=""):
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
                    lines[line_num]+="& \\multirow{{{}}}{{*}}{{ {} }}  ".format(partial,sum(datarow[line_num:line_num+partial]))
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
                    suffix+="\\cline{{{}-{}}}".format(num+1,num+1)
            i+=1
        lines[line_num]+="\\\\{}\n".format(suffix)
    
    ltable="".join(lines)

    if partial_labels:
        header=( (" & {}"*len(partial_labels)).format(*partial_labels) )*len(data)+" \\\\\\hline\n"
        ltable=header+ltable
    if datarow_labels:
        header=((" & \\multicolumn{{%i}}{{c|}}{{{}}}"%(len(partials),))*len(datarow_labels)).format(*datarow_labels)+" \\\\\\hline\n"
        ltable=header+ltable
    header="\\begin{center}\n\\begin{tabular}{l ||"+" c |"*len(data)*len(partials)+"}\\hline\n"
    footer="\\end{tabular}\n\\end{center}"
    ltable=header+ltable+footer
    return ltable

def pcaTable(pca_evolution):
    """Make table with PCA formation mean and std"""
    pass

def writeTex(string,filename):
    with open(filename,"w") as f:
        f.write(string)
