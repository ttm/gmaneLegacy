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

# wn.morph eh um lematizador

# wn.path_similarity dah a similatidade pela proximidade na arvore taxonomica

# wn.res_similarity dah a similatidade dados dois synsets e ic

# wp.wup_symilarity dah a similaridade dados 2 synsets

###############
####### para um synset
ss=wn.synsets("banana")
#3[Synset('banana.n.01'), Synset('banana.n.02')]
sb=ss[0]

# sb.also_sees nao retorna nada
# sb.attributes retorna nada
# sb.hypernym_distances com as arvores ateh conceito mais geral
# sb.hypernym_paths retorna lista de caminhos ateh a raiz
# sb.lemmas retorna os lemas associados aas palavras
# sb.offset retorna inteiro provavelmente para referenciamento interno
# sb.similar_tos retorna nada
# sb.lexname retorna classificação: classe gramatical.semantica ****
# sb.part_holonyms retorna 
# sb.substance_holonyms retorna nada
# sb.causes retorna nada
# sb.hypernyms os hiperonimos imediatos
# sb.lin_similarity
# sb.part_meronyms alguns retornam meronimias
# sb.substance_meronyms alguns retornam meronimias
# sb.closure retorna a cadeia com fechamento pela relação dada
# sb.hyponyms retorna os hiponimos imediatos
# sb.lowest_common_hypernyms
# sb.path_similarity 
# sb.topic_domains alguns synset retornam outros synsets, parecem um tipo de holonímia
# sb.common_hypernyms *********************
# sb.instance_hypernyms retorna alguns hypernônimos
# sb.max_depth tamanho do maior caminho aa raiz ***********
# sb.pos  retorna o part of speech do synset **********
# sb.tree retorna árvore segundo critério
# sb.definition  ***
# sb.instance_hyponyms instance?
# sb.member_holonyms member?
# sb.member_meronyms
# sb.region_domains nada ?
# sb.unicode_repr
# sb.entailments nada ?  para verbos tem as consequencias
# sb.jcn_similarity
# sb.res_similarity 
# sb.usage_domains nada ?
# sb.examples frases de exemplo de uso do synset
# sb.lch_similarity    
# sb.min_depth   ***********
# sb.root_hypernyms  *********    
# sb.verb_groups retornam o que parecem ser hiperonimos verbais ****
# sb.frame_ids alguns synsets retornam sequências de inteiros ??? **
# sb.lemma_names retorna o que parecem ser nomes que representam ?
# sb.name o nome do synset
# sb.shortest_path_distance
# sb.wup_similarity

# dúvidas: algumas funcoes que retornam pouco ou nada
# algumas especificacoes, como member, instace, usage e topic, part e substance

# k.corpus.wordnet_ic parece que abre information content prontos ou a partir de outros corpus:
# http://www.nltk.org/howto/wordnet.html    

# qual a diferença entre lemma e synset?


# wn.synsets("run")
#[Synset('banana.n.01'), Synset('banana.n.02')]
# [Synset('run.n.01'), Synset('test.n.05'), Synset('footrace.n.01'), Synset('streak.n.01'), Synset('run.n.05'), Synset('run.n.06'), Synset('run.n.07'), Synset('run.n.08'), Synset('run.n.09'), Synset('run.n.10'), Synset('rivulet.n.01'), Synset('political_campaign.n.01'), Synset('run.n.13'), Synset('discharge.n.06'), Synset('run.n.15'), Synset('run.n.16'), Synset('run.v.01'), Synset('scat.v.01'), Synset('run.v.03'), Synset('operate.v.01'), Synset('run.v.05'), Synset('run.v.06'), Synset('function.v.01'), Synset('range.v.01'), Synset('campaign.v.01'), Synset('play.v.18'), Synset('run.v.11'), Synset('tend.v.01'), Synset('run.v.13'), Synset('run.v.14'), Synset('run.v.15'), Synset('run.v.16'), Synset('prevail.v.03'), Synset('run.v.18'), Synset('run.v.19'), Synset('carry.v.15'), Synset('run.v.21'), Synset('guide.v.05'), Synset('run.v.23'), Synset('run.v.24'), Synset('run.v.25'), Synset('run.v.26'), Synset('run.v.27'), Synset('run.v.28'), Synset('run.v.29'), Synset('run.v.30'), Synset('run.v.31'), Synset('run.v.32'), Synset('run.v.33'), Synset('run.v.34'), Synset('ply.v.03'), Synset('hunt.v.01'), Synset('race.v.02'), Synset('move.v.13'), Synset('melt.v.01'), Synset('ladder.v.01'), Synset('run.v.41')]
# os verbos só aparecem depois.
# talvez seja necessário pegar da etiquetação POS
# e achar o synset com tipo certo e numeração mais baixa.





