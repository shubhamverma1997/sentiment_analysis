import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
from textblob import Word


if __name__ == "__main__":

	seedList = [['good', 1],['bad', -1], ['Love', 1], ['hate', -1]]
	graph=nx.Graph()
	adjList= []

	for seed in seedList:
		graph.add_node(seed[0])
		adjList.append(seed[0])		
	
	i=1
	while i<=4:		
		for a in adjList:
			temp = []
			for syn in wn.synsets(a):				#synonyms
				word=syn.lemma_names()[0]
				if word not in graph.nodes():
					graph.add_node(word)
					graph.add_edge(a,word,weight=1)
					temp.append(word)

			syn=Word(a).synsets[0]

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					graph.add_node(anyt.name())		#antonyms
					graph.add_edge(a,anyt.name(),weight=-1)
					temp.append(anyt.name())

			for hypr in syn.hypernyms():
				graph.add_node(hypr.lemma_names()[0])	#hypernyms
				graph.add_edge(a,hypr.lemma_names()[0],weight=1)
				temp.append(hypr.lemma_names()[0])

			for hypo in syn.hyponyms():
				graph.add_node(hypo.lemma_names()[0]) 	#hyponyms
				graph.add_edge(a,hypo.lemma_names()[0],weight=1)
				temp.append(hypo.lemma_names()[0])

			adjList=temp

		i=i+1
	
	nx.draw(graph,pos=nx.random_layout(graph), with_labels=True, node_color='#ADD8E6', font_size=6, width=0.2)

	plt.savefig("mlpro.png")






