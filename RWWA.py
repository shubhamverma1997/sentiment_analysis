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
		anytseed=[]
		hyprseed=[]
		hyposeed=[]
		for syn in wn.synsets(seed[0]):
			synseed.append(syn.lemma_names()[0])	#synonyms

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					anytseed.append(anyt.name())	#antonyms

			for hypr in syn.hypernyms():
				hyprseed.append(hypr.lemma_names()[0])	#hypernyms

			for hypo in syn.hyponyms():
				hyposeed.append(hypo.lemma_names()[0])	#hyponyms

		for a in adjList:
			add=[a,seed[1]]
			if a in synseed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
			if a in synseed:
				graph.add_edge(seed[0],a,weight=1)

			add=[a,-seed[1]]
			if a in anytseed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
			if a in anytseed:
				graph.add_edge(seed[0],a,weight=-1)

			add=[a,seed[1]]
			if a in hyprseed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
			if a in hyprseed:
				graph.add_edge(seed[0],a,weight=1)

			add=[a,seed[1]]
			if a in hyposeed and add not in seedList:
				seedList.append(add)
				graph.add_node(a)
			if a in hyposeed:
				graph.add_edge(seed[0],a,weight=1)


if __name__ == "__main__":

	seedList = [['good', 1],['bad', -1], ['Love', 1], ['hate', -1]]
	graph=nx.Graph()
	posList = []
	negList = []
	neutList = []
	adjList= []

	for seed in seedList:
		graph.add_node(seed[0])
		adjList.append(seed[0])		

	i=0
	while i<2:		
		for a in adjList:
			temp = []
			for syn in wn.synsets(a):
				if syn.lemma_names()[0] not in adjList:
					temp.append(syn.lemma_names()[0])

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					temp.append(anyt.name())	#antonyms

			for hypr in syn.hypernyms():
				temp.append(hypr.lemma_names()[0])	#hypernyms

			for hypo in syn.hyponyms():
				temp.append(hypo.lemma_names()[0])

			adjList=adjList+temp
		i=i+1

	Orntpred(adjList,seedList)	#First function call	

	# labels=nx.get_edge_attributes(graph,'weight')
	
	nx.draw(graph,pos=nx.random_layout(graph), with_labels=True, node_color='#ADD8E6', font_size=8, width=0.5)	

	# nx.draw_networkx_edge_labels(graph,pos=nx.circular_layout(graph),edge_labels=labels,font_size=6)

	plt.savefig("walk.png")






