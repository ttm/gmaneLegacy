import nltk as k, pickle, time, sys
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
training_data = treebank.tagged_sents()[:100]
baseline_data = treebank.tagged_sents()[100:200]
gold_data = treebank.tagged_sents()[200:300]
#testing_data = [untag(s) for s in gold_data]
testing_data = [[ss[0] for ss in s] for s in gold_data]

backoff = RegexpTagger([
(r'^-?[0-9]+(.[0-9]+)?$', 'NUM'),   # cardinal numbers
(r'(The|the|A|a|An|an)$', 'DET'),   # articles
(r'.*able$', 'ADJ'),                # adjectives
(r'.*ness$', 'NOUN'),                # nouns formed from adjectives
(r'.*ly$', 'ADV'),                  # adverbs
(r'.*s$', 'NOUN'),                  # plural nouns
(r'.*ing$', 'VERB'),                # gerunds
(r'.*ed$', 'VERB'),                 # past tense verbs
(r'.*', 'NOUN')                      # nouns (default)
])

baseline = backoff
baseline.evaluate(gold_data)

Template._cleartemplates() #clear any templates created in earlier tests
templates = [Template(Pos([-1])), Template(Pos([-1]), Word([0]))]

tt = BrillTaggerTrainer(baseline, templates, trace=3)

tagger1 = tt.train(training_data, max_rules=10)
tagger1.rules()[1:3]
train_stats = tagger1.train_stats()

tagger1.print_template_statistics(printunused=False)

tagger1.evaluate(gold_data)
tagged, test_stats = tagger1.batch_tag_incremental(testing_data, gold_data)

tagger2 = tt.train(training_data, max_rules=10, min_acc=0.99)

print(tagger2.evaluate(gold_data))  # doctest: +ELLIPSIS
tagger2.rules()[2:4]

#nn_cd_tagger = k.tag.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),                                       (r'.*', 'NN')])
nn_cd_tagger = baseline
#tagged_data = k.corpus.treebank.tagged_sents()
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
print("Done loading.")
atime=time.time()
unigram_tagger = k.tag.UnigramTagger(training_data,backoff=nn_cd_tagger)
bigram_tagger = k.tag.BigramTagger(training_data,
                                 backoff=unigram_tagger)

trigram_tagger = k.tag.TrigramTagger(training_data,
                                 backoff=bigram_tagger)
print("Done ngrams.",time.time()-atime); atime=time.time()#
##templates = [
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,1)),
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (2,2)),
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,2)),
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,3)),
##
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,1)),
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (2,2)),
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,2)),
##  k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,3)),
##
##  k.tag.brill.ProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (-1, -1), (1,1)),
##  k.tag.brill.ProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (-1, -1), (1,1)),
##  ]
trace=2
trainer = k.tag.BrillTaggerTrainer(trigram_tagger, templates, trace)
print("Done bootstrapping trainer.",time.time()-atime); atime=time.time()#)
#trainer = k.tag.brill.BrillTaggerTrainer(bigram_tagger, trace)
##trainer = brill.BrillTaggerTrainer(u, templates, trace)
max_rules=40000
min_score=1
brill_tagger = trainer.train(training_data, max_rules, min_score)
print("Done training.",time.time()-atime); atime=time.time()#)
 
f=open("./pickledir/brill_tagger2", 'wb')
pickle.dump(brill_tagger_,f,-1)
f.close()
print("Done writting.",time.time()-atime); atime=time.time()#)
# acerto de: 0.9184661557159511
