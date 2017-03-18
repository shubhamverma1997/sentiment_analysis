import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
from textblob import Word
from random import choice
import numpy as np


def transit_P (i,j,graph):
	nbrs=graph.neighbors(i)
	wtsum=0
	for nb in nbrs:
		wt=(Word(i).synsets[0]).path_similarity(Word(nb).synsets[0])
		if wt==None:
			wt=0
		wtsum=wtsum+wt
	return ((Word(i).synsets[0]).path_similarity(Word(j).synsets[0]))/wtsum

def hit2plus(i,splus,graph):
	if i in splus:
		return 0
	else:		
		sum=0
		for j in graph.nodes():
			sum=sum+transit_P(i,j,graph)*(hit2plus(j,splus,graph)+1)
		return sum	

def hit2minus(i,sminus,graph):
	if i in sminus:
		return 0
	else:		
		sum=0
		for j in graph.nodes():
			sum=sum+transit_P(i,j,graph)*(hit2minus(j,sminus,graph)+1)
		return sum

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
					graph.add_edge(a,word)
					temp.append(word)

			syn=Word(a).synsets[0]

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					if anyt.name() not in graph.nodes():						
						graph.add_node(anyt.name())		#antonyms
						graph.add_edge(a,anyt.name())
						temp.append(anyt.name())

			for hypr in syn.hypernyms():
				if hypr.lemma_names()[0] not in graph.nodes():
					graph.add_node(hypr.lemma_names()[0])	#hypernyms
					graph.add_edge(a,hypr.lemma_names()[0])
					temp.append(hypr.lemma_names()[0])

			for hypo in syn.hyponyms():
				if hypo.lemma_names()[0] not in graph.nodes():					
					graph.add_node(hypo.lemma_names()[0]) 	#hyponyms
					graph.add_edge(a,hypo.lemma_names()[0])
					temp.append(hypo.lemma_names()[0])

			adjList=temp

		i=i+1
	nx.draw(graph,pos=nx.random_layout(graph),with_labels=True, node_color='#ADD8E6', font_size=5, width=0.2, alpha=0.4)

	plt.savefig("RnWalk.png", dpi=1000)

	known = seedList
	splus = []
	sminus = []
	for kn in known:
		if kn[1]==1:
			splus.append(kn[0])
		if kn[1]==-1:
			sminus.append(kn[0])

	unknown = []
	for w in graph.nodes():
		if w not in known:
			unknown.append(w)

	for w in unknown:
		avg_pos=0
		avg_neg=0
		k=1
		while k<=5:
			htime=hit2plus(w,splus,graph)
			avg_pos=avg_pos+htime
			k=k+1
		avg_pos=avg_pos/5

		k=1
		while k<=5:
			htime=hit2minus(w,sminus,graph)
			avg_neg=avg_neg+htime
			k=k+1
		avg_neg=avg_neg/5

		if avg_pos>avg_neg:
			seedList.append([w,1])
		else:
			seedList.append([w,-1])

	print(seedList)
