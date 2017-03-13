import nltk
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
filename=open("review1.txt")
raw=filename.read()

tokens=nltk.word_tokenize(raw)
print tokens

tokens = [i for i in tokens if len(wn.synsets(i)) > 0]
filterred=[word for word in tokens if word not in stopwords.words('english')]
tagged=nltk.pos_tag(filterred)
print(tagged)

pscore=0
nscore=0

for i in range(0,len(tagged)):
	text=tagged[i][0]
	if 'NN' in tagged[i][1] :
		score=swn.senti_synset(text+'.n.01')
		pscore+=score.pos_score()
		nscore+=score.neg_score()
	elif 'VB' in tagged[i][1] :
		score=swn.senti_synset(text+'.v.01')
		pscore+=score.pos_score()
		nscore+=score.neg_score()
	elif 'JJ' in tagged[i][1] :
		score=swn.senti_synset(text+'.a.01')
		pscore+=score.pos_score()
		nscore+=score.neg_score()
	elif 'RB' in tagged[i][1] :
		score=swn.senti_synset(text+'.r.01')
		pscore+=score.pos_score()
		nscore+=score.neg_score()		
	else : continue
print("\nPositivity : ")
print(pscore)
print("\nNegatitivity : ")
print(nscore)