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
	while i<=1:
		temp = []	
		for a in adjList:			
			for syn in wn.synsets(a):				#synonyms
				word=syn.lemma_names()[0]
				if word not in graph.nodes():
					graph.add_node(word)
					wt=syn.path_similarity(Word(a).synsets[0])
					if wt==None:
						wt=0
					graph.add_edge(a,word,weight=round(wt,2))
					temp.append(word)

			syn=Word(a).synsets[0]

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					if anyt.name() not in graph.nodes():						
						graph.add_node(anyt.name())		#antonyms
						wt=syn.path_similarity(Word(anyt.name()).synsets[0])
						if wt==None:
							wt=0
						graph.add_edge(a,anyt.name(),weight=round(wt,2))
						temp.append(anyt.name())

			for hypr in syn.hypernyms():
				if hypr.lemma_names()[0] not in graph.nodes():
					graph.add_node(hypr.lemma_names()[0])	#hypernyms
					wt=syn.path_similarity(Word(hypr.lemma_names()[0]).synsets[0])
					if wt==None:
						wt=0
					graph.add_edge(a,hypr.lemma_names()[0],weight=round(wt,2))
					temp.append(hypr.lemma_names()[0])

			for hypo in syn.hyponyms():
				if hypo.lemma_names()[0] not in graph.nodes():					
					graph.add_node(hypo.lemma_names()[0]) 	#hyponyms
					wt=syn.path_similarity(Word(hypo.lemma_names()[0]).synsets[0])
					if wt==None:
						wt=0
					graph.add_edge(a,hypo.lemma_names()[0],weight=round(wt,2))
					temp.append(hypo.lemma_names()[0])

			adjList=temp

		i=i+1
	nx.draw(graph,pos=nx.random_layout(graph),with_labels=True, node_color='#ADD8E6', font_size=5, width=0.2, alpha=0.4)

	plt.savefig("RnWalk.png", dpi=1000)






