import os
import gmaneLegacy as g
from collections import OrderedDict

TDIR="/home/r/repos/artigoTextoNasRedes3/tables/SI2/"
files=os.listdir(TDIR)
files = [i for i in files if 'charsInline' in i and '_' not in i and
        'Total' not in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline\\hline\\hline',
            '\\hline').replace('\\hline\\hline',
                    '\\hline').split('\\\\\\hline')[3:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'charsInlineTotal.tex'
caption = 'Counts of evidence of characters-related differences in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,3,5,6])

# ========================================

files=os.listdir(TDIR)
files = [i for i in files if 'tokensMergedInline' in i and '_' not in i
        and 'Total' not in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[4:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'tokensMergedInlineTotal.tex'
caption = 'Counts of evidence of token-related differences in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,3,4,5,7,9,11,13])
 
# ========================================

files=os.listdir(TDIR)
files = [i for i in files if 'sentencesInline' in i and '_' not in i
        and 'Total' not in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[3:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'sentencesInlineTotal.tex'
caption = 'Counts of evidence of sentence-related differences in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,6,8,10])
 
# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'messagesInline' in i and '_' not in i
        and 'Total' not in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[3:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'messagesInlineTotal.tex'
caption = 'Counts of evidence of message-related differences in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,6,8,10,12])
 
# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'posInline' in i and '_' not in i
        and 'Total' not in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[1:-2]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'posInlineTotal.tex'
caption = 'Counts of evidence of differences related to POS tags in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,7,9,10,11])
 
# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'wnPOSInline' in i and '_' not in i
        and 'Total' not in i and '-' not in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[1:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'wnPOSInlineTotal.tex'
caption = 'Counts of evidence of differences related to Wordnet POS tags in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1,-4],[1,4],)
 
# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'wnPOSInline2-n-' in i and '_' not in i
        and 'Total' not in i and 'tag' in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[1:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'wnPOSInline2-n-Total.tex'
caption = 'Counts of evidence of differences related to Wordnet noun synset characteristics in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,6,8,10,12,14,16])

# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'wnPOSInline2-as-' in i and '_' not in i
        and 'Total' not in i and 'tag' in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[1:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'wnPOSInline2-as-Total.tex'
caption = 'Counts of evidence of differences related to Wordnet adjective synset characteristics in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,6,8])
 
# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'wnPOSInline2-v-' in i and '_' not in i
        and 'Total' not in i and 'tag' in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[1:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'wnPOSInline2-v-Total.tex'
caption = 'Counts of evidence of differences related to Wordnet verb synset characteristics in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,6,8,10,12,14,16])

# ---------------------------------- 

files=os.listdir(TDIR)
files = [i for i in files if 'wnPOSInline2-r-' in i and '_' not in i
        and 'Total' not in i and 'tag' in i]
adict = {1:OrderedDict(), 2:{}, 3:{}}

for afile in files:
    text = open(TDIR+afile,'r').read().replace('\\hline','').split('\\\\')[1:-1]
    # t = [i[1:-1] for i in text if ' total' not in i]
    t = [i[1:-1] for i in text]
    t_ = [i.split(' & ') for i in t]
    matrix = [[float(i) for i in j[2:]] for j in t_]
    names = [i[0] for i in t_]
    layer = 1
    for array, name in zip(matrix, names):
        if ' total' in name:
            layer += 1
            continue
        if min(array) == 0:
            continue
        if max(array) < 5:
            low_measure = 1
        elif max(array) < 10:
            low_measure = 2
        else:
            low_measure = 0
        if max(array)/min(array) > 1.5:
            difference = 2
        elif max(array)/min(array) > 1.1:
            difference = 1
        else:
            difference = 0
        array_ = sorted(array)
        a = array
        if sum([i==j for i,j in zip(array, array_)]) == 3:
            order = 'h'
        elif sum([i==j for i,j in zip([a[2], a[0], a[1]], array_[::-1])]) == 3:
            order = 'hp'
        elif sum([i==j for i,j in zip(array, array_[::-1])]) == 3:
            order = 'p'
        elif sum([i==j for i,j in zip([a[0], a[2], a[1]], array_[::-1])]) == 3:
            order = 'ph'
        elif sum([i==j for i,j in zip([a[1], a[0], a[2]], array_[::-1])]) == 3:
            order = 'ip'
        elif sum([i==j for i,j in zip([a[1], a[2], a[0]], array_[::-1])]) == 3:
            order = 'ih'

        print(array)
        print(name, difference, low_measure, order)
        if difference == 0:
            order = '-'
        elif difference == 2:
            order += '*'
        if low_measure == 2:
            order += '_'
        elif low_measure == 1:
            order += '__'
        print(order)
        if name in adict[layer]:
            adict[layer][name].append(order)
        else:
            adict[layer][name] = [order]
adict_ = {1:OrderedDict(), 2:{}, 3:{}}
adict2 = {1:OrderedDict(), 2:{}, 3:{}}
adict3 = {1:OrderedDict(), 2:{}, 3:{}}
adict4 = {1:OrderedDict(), 2:{}, 3:{}}
adict5 = {1:OrderedDict(), 2:{}, 3:{}}
adict6 = {1:OrderedDict(), 2:{}, 3:{}}
print('\n\n\n =========================')
for layer in adict:
    for synset in adict[layer]:
        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict_[layer][synset] = ((per, inte, hubs), peaks)

        measures = adict[layer][synset]
        per = sum([i[0]=='p' for i in measures])
        inte = sum([i[0]=='i' for i in measures])
        hubs = sum([i[0]=='h' for i in measures])
        peaks = sum(['hp' in i or 'ph' in i for i in measures])+inte
        adict2[layer][synset] = ((per, inte, hubs), peaks)

        measures_ = [i for i in measures if '_' not in i]
        per = sum([i[0]=='p' for i in measures_])
        inte = sum([i[0]=='i' for i in measures_])
        hubs = sum([i[0]=='h' for i in measures_])
        peaks_ = sum(['hp' in i or 'ph' in i for i in measures_])+inte
        adict3[layer][synset] = ((per, inte, hubs), peaks_)

        total = [0, 0, 0]
        for measure in measures:
            val = 1
            if '_' in measure:
                val *=.5
                print('times .5 ===========<')
            if '*' in measure:
                val *= 2
            if measure[0] == 'p':
                total[0] += val
            elif measure[0] == 'i':
                total[1] += val
            elif measure[0] == 'h':
                total[2] += val

        adict4[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))
        adict5[layer][synset] = (total, adict2[layer][synset][0],
                (peaks, len(measures)), measures)
        # if len(measures) >= 13:
        adict6[layer][synset] = (total, adict2[layer][synset][0], (peaks, len(measures)))

labelsh = ['synset', 'p.', 'i.', 'h', 'peaks']
labels = []
data = []
for layer in adict6:
    for entry in adict6[layer]:
        labels.append(entry)
        data_ = adict6[layer][entry]
        data.append([*data_[1], *data_[2]][:-1])
fname_ = TDIR+'wnPOSInline2-r-Total.tex'
caption = 'Counts of evidence of differences related to Wordnet adverb synset characteristics in the Erd\\"os sectors in each of the analyzed networks.'
g.tableHelpers.lTable(labels,labelsh,data,caption,fname_,two_decimal=False)
ME=g.tableHelpers.me
ME(fname_[:-4],"\\bf",[(0,i) for i in range(0,5)])
DL=g.tableHelpers.dl
DL(fname_[:-4]+"_",[1],[1,4],[2,4,6])
