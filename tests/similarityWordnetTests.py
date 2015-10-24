from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(["I'd like an apple",
                            "An apple a day keeps the doctor away",
                            "Never compare an apple to an orange",
                            "I prefer scikit-learn to Orange"])
aa=(tfidf * tfidf.T).A
#array([[ 1.        ,  0.25082859,  0.39482963,  0.        ],
#       [ 0.25082859,  1.        ,  0.22057609,  0.        ],
#       [ 0.39482963,  0.22057609,  1.        ,  0.26264139],
#       [ 0.        ,  0.        ,  0.26264139,  1.        ]])

# jah a wordnet tem synset de cada palavra, algo mais?
# o que quer dizer cada métodos do synset?
# quais as medidas razoáveis?
# conseguimos saber quais os hiperonimos mais incidentes?
# convém alguma outra medida?


from nltk.corpus import wordnet as wn
#kwss=[i for i in kw if wn.synsets(i)] #

# ver melhor como usar wn.ic

# wn.jcn_similarity coalcula similaridade entre dois sentidos de palavras
# recebe dois synsets e um ic

# wn.synsets("viajem",lang="por")

# wn.lch_similarity mede similaridade só com 2 synsets

# wn.lemma("banana") dah erro
# _count e _from_key, ambos dão erro

# wn.lin_similarity(synset1, synset2, ic, verbose=False)

# wn.lin_similarity dá o quão similar são dois synsets
# dado ic
