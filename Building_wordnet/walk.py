import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

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

		hyprseed=[]
		syn = wn.synsets(seed[0])
		for s in syn:
			for hypr in s.hypernyms():
				hyprseed.append(hypr.lemma_names()[0])

		hyposeed=[]
		syn = wn.synsets(seed[0])
		for s in syn:
			for hypo in s.hyponyms():
				hyposeed.append(hypo.lemma_names()[0])

		for a in adjList:
			add=[a,seed[1]]
			if a in synseed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
				graph.add_edge(seed[0],a)

		for a in adjList:
			add=[a,-seed[1]]
			if a in anytseed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
				graph.add_edge(seed[0],a)

		for a in adjList:
			add=[a,seed[1]]
			if a in hyprseed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
				graph.add_edge(seed[0],a)

		for a in adjList:
			add=[a,seed[1]]
			if a in hyposeed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
				graph.add_edge(seed[0],a)


if __name__ == "__main__":

	seedList = [['good', 1],['wrong', -1], ['complete', 1], ['ill', -1], ['happy', 1],['foolish', -1], ['cute', 1],['computer', 1],['canine', 1]]
	graph=nx.Graph()
	posList = []
	negList = []
	neutList = []
	for seed in seedList:
		graph.add_node(seed[0])

	f = open('Words1.txt')
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
	f=open('seeds_trained.txt','w')
	f.write(str(seedList))
	print('\nAdjectives List\n')
	print(adjList)

	for seed in seedList:
		if seed[1]==1:
			posList.append(seed[0])
		elif seed[1]==-1:
			negList.append(seed[0])
		elif seed[1]==0:
			neutList.append(seed[0])
			

	nx.draw(graph, pos=nx.circular_layout(graph), nodelist=posList, node_color='g', alpha=0.9, font_size=8, width=0.5, with_labels=True)

	nx.draw(graph, pos=nx.circular_layout(graph), nodelist=negList, node_color='r', alpha=0.9, font_size=8, width=0.5, with_labels=True)

	nx.draw(graph, pos=nx.circular_layout(graph), nodelist=neutList, node_color='b', alpha=0.9, font_size=8, width=0.2, with_labels=True)

	plt.savefig("walk.png")






