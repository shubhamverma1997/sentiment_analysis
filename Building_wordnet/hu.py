import nltk
from nltk.corpus import wordnet as wn
hyper=[]
hypo=[]
def Orntpred(adjList,seedList):		
	while True:							
		size1=len(seedList)			#Check length of seedlist before
		Orntsrch(adjList,seedList)
		size2=len(seedList)			#Check length of seedlist after

		if size2==size1:			#If none added to seedlist from adjective list, abort!
			return

def Orntsrch(adjList,seedList):
	for seed in seedList:
		synseed = []
		for syn in wn.synsets(seed[0]):
			synseed.append(syn.lemma_names()[0])

		anytseed=[]
		for syn in wn.synsets(seed[0]):
			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					anytseed.append(anyt.name())
		
		for h in wn.synsets(seed[0]):
			if h.hypernyms():
				hyper.append(h.hypernyms()[0])

		for h in wn.synsets(seed[0]):
			if h.hyponyms():				
				hypo.append(h.hyponyms()[0])

		for a in adjList:
			add=[a,seed[1]]
			if a in synseed and add not in seedList:
				seedList.append(add)

		for a in adjList:
			add=[a,-seed[1]]
			if a in anytseed and add not in seedList:
				seedList.append(add)
			
if __name__ == "__main__":

	seedList = []
	seedList.append(['good', 1])
	seedList.append(['wrong', -1])   #Seed list of two words with given Orientation

	f = open('Words.txt')
	raw=f.read()
	adj = nltk.word_tokenize(raw)

	adjList= []		#Adjectives list of words imported from txt file and given default orientation of 0

	for a in adj:	
		adjList.append(a) 

	print('\nSeedList\n')
	print(seedList)
	print('\nAdjectives List\n')
	print(adjList)
	print('\n')

	Orntpred(adjList,seedList)	#First function call

	print('\nSeedList\n')
	print(seedList)
	print('\nAdjectives List\n')
	print(adjList)
	print("\nHypernyms\n")	
	print(hyper)
	print("\nHyponyms\n")
	print(hypo)
	
	




