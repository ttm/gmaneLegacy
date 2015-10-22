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




#training_data = treebank.tagged_sents()[:100]
#baseline_data = treebank.tagged_sents()[100:200]
#gold_data = treebank.tagged_sents()[200:300]
##testing_data = [untag(s) for s in gold_data]
#testing_data = [[ss[0] for ss in s] for s in gold_data]
#
#backoff = RegexpTagger([
#(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
#(r'(The|the|A|a|An|an)$', 'AT'),   # articles
#(r'.*able$', 'JJ'),                # adjectives
#(r'.*ness$', 'NN'),                # nouns formed from adjectives
#(r'.*ly$', 'RB'),                  # adverbs
#(r'.*s$', 'NNS'),                  # plural nouns
#(r'.*ing$', 'VBG'),                # gerunds
#(r'.*ed$', 'VBD'),                 # past tense verbs
#(r'.*', 'NN')                      # nouns (default)
#])
#
#baseline = backoff
#baseline.evaluate(gold_data)
#
#Template._cleartemplates() #clear any templates created in earlier tests
#templates = [Template(Pos([-1])), Template(Pos([-1]), Word([0]))]
#
#tt = BrillTaggerTrainer(baseline, templates, trace=3)
#
#tagger1 = tt.train(training_data, max_rules=10)
#tagger1.rules()[1:3]
#train_stats = tagger1.train_stats()
#
#tagger1.print_template_statistics(printunused=False)
#
#tagger1.evaluate(gold_data)
#tagged, test_stats = tagger1.batch_tag_incremental(testing_data, gold_data)
#
#tagger2 = tt.train(training_data, max_rules=10, min_acc=0.99)
#
#print(tagger2.evaluate(gold_data))  # doctest: +ELLIPSIS
#tagger2.rules()[2:4]
#
##nn_cd_tagger = k.tag.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),                                       (r'.*', 'NN')])
#nn_cd_tagger = baseline
##tagged_data = k.corpus.treebank.tagged_sents()
#tagged_data = k.corpus.treebank.tagged_sents(tagset="universal")
#tagged_data2 = k.corpus.brown.tagged_sents(tagset="universal")
#num_sents=len(tagged_data)
#num_sents2=len(tagged_data2)
#train=0.8
#cutoff = int(num_sents *train)
#cutoff2 = int(num_sents2*train)
#training_data = tagged_data[:cutoff]+tagged_data2[:cutoff2]
#gold_data = tagged_data[cutoff:]+tagged_data2[cutoff2:]
#testing_data = [[t[0] for t in sent] for sent in gold_data]
#print("Done loading.")
#unigram_tagger = k.tag.UnigramTagger(training_data,backoff=nn_cd_tagger)
#bigram_tagger = k.tag.BigramTagger(training_data,
#                                 backoff=unigram_tagger)
###templates = [
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,1)),
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (2,2)),
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,2)),
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,3)),
###
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,1)),
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (2,2)),
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,2)),
###  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,3)),
###
###  k.tag.brill.ProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (-1, -1), (1,1)),
###  k.tag.brill.ProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (-1, -1), (1,1)),
###  ]
#trace=5 
#trainer = k.tag.BrillTaggerTrainer(bigram_tagger, templates, trace)
##trainer = k.tag.brill.BrillTaggerTrainer(bigram_tagger, trace)
###trainer = brill.BrillTaggerTrainer(u, templates, trace)
#max_rules=40000
#min_score=2
#brill_tagger = trainer.train(training_data, max_rules, min_score)
# 
#f=open("./pickledir/brill_tagger", 'wb')
#pickle.dump(brill_tagger,f,-1)
#f.close()
