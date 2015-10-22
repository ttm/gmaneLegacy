import nltk as k, pickle

tagger=k.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')
# levou muito tempo, retornou:
# tagger.evaluate(k.corpus.brown.tagged_sents())
# 0.5952331741865255
# pq as tags não são as mesmas?

# Receita do Brill na própria classe do nltk

from nltk.tbl.template import Template
from nltk.tag.brill import Pos, Word
from nltk.tag import RegexpTagger, BrillTaggerTrainer
from nltk.corpus import treebank

f=open("pickledir/brill_tagger","rb")
brill_tagger=pickle.load(f)
f.close()
f=open("pickledir/brill_tagger2","rb")
brill_tagger2=pickle.load(f)
f.close()
f=open("pickledir/brill_tagger3","rb")
brill_tagger3=pickle.load(f)
f.close()
f=open("pickledir/brill_tagger4","rb")
brill_tagger4=pickle.load(f)
f.close()
f=open("pickledir/brill_tagger5","rb")
brill_tagger5=pickle.load(f)
f.close()

tagged_data = k.corpus.treebank.tagged_sents(tagset="universal")
tagged_data2 = k.corpus.brown.tagged_sents(tagset="universal")
num_sents=len(tagged_data)
num_sents2=len(tagged_data2)
train=0.8
cutoff = int(num_sents *train)
cutoff2 = int(num_sents2*train)
training_data = tagged_data[:cutoff]+tagged_data2[:cutoff2]
gold_data = tagged_data[cutoff:]+tagged_data2[cutoff2:]
testing_data = [[t[0] for t in sent] for sent in gold_data]

#import timeit
#print("before")
#print(timeit.timeit("brill_tagger.tag_sents(testing_data[400:600])",number=1000))
#print("after",time.time()-atime)

#In [85]: %timeit brill_tagger.tag_sents(testing_data[400:430])
#100 loops, best of 3: 8.67 ms per loop
#In [88]: brill_tagger.evaluate(gold_data)
#Out[88]: 0.9188828533869088
#
#In [86]: %timeit brill_tagger2.tag_sents(testing_data[400:430])
#100 loops, best of 3: 12.4 ms per loop
#In [88]: brill_tagger.evaluate(gold_data)
# 0.9188828533869088
#
#In [87]: %timeit brill_tagger3.tag_sents(testing_data[400:430]) ### MELHOR
#10 loops, best of 3: 42 ms per loop
#In [3]: brill_tagger3.evaluate(gold_data)
#Out[3]: 0.9188977354465858

#In [5]: %timeit brill_tagger4.tag_sents(testing_data[400:430])
#10 loops, best of 3: 48.4 ms per loop
#In [3]: brill_tagger4.evaluate(gold_data)
#Out[3]: 0.9187141900439021

#In [7]: %timeit brill_tagger5.tag_sents(testing_data[400:430])
#10 loops, best of 3: 48.4 ms per loop
#In [88]: brill_tagger.evaluate(gold_data)
#Out[88]: 0.918709229357343




