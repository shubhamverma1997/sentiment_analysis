import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
from textblob import Word
from random import choice
import numpy as np
from random import random
from bisect import bisect

def transit_P (i,j,graph):
	nbrs=graph.neighbors(i)
	wtsum=0
	for nb in nbrs:
		wt=graph[i][nb]['weight']
		wtsum=wtsum+wt
	return graph[i][j]['weight']/wtsum

def hit2plus(i,splus,graph,count):
	if i in splus:
		return count
	elif len(graph.neighbors(i))==0:
		return 0
	else:
		probs = []
		for j in graph.neighbors(i):
			probs.append(transit_P(i,j,graph))
		draw = np.random.choice(graph.neighbors(i), p=probs)
		return hit2plus(draw,splus,graph,count+1)	

def hit2minus(i,sminus,graph,count):
	if i in sminus:
		return count
	elif len(graph.neighbors(i))==0:
		return 0
	else:
		probs = []
		for j in graph.neighbors(i):
			probs.append(transit_P(i,j,graph))
		draw = np.random.choice(graph.neighbors(i), p=probs)
		return hit2minus(draw,sminus,graph,count+1)	

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
					graph.add_edge(a,word,weight=1)
					temp.append(word)

			syn=Word(a).synsets[0]

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					if anyt.name() not in graph.nodes():						
						graph.add_node(anyt.name())		#antonyms
						graph.add_edge(a,anyt.name(),weight=-1)
						temp.append(anyt.name())

			for hypr in syn.hypernyms():
				if hypr.lemma_names()[0] not in graph.nodes():
					graph.add_node(hypr.lemma_names()[0])	#hypernyms
					graph.add_edge(a,hypr.lemma_names()[0],weight=1)
					temp.append(hypr.lemma_names()[0])

			for hypo in syn.hyponyms():
				if hypo.lemma_names()[0] not in graph.nodes():					
					graph.add_node(hypo.lemma_names()[0]) 	#hyponyms
					graph.add_edge(a,hypo.lemma_names()[0],weight=1)
					temp.append(hypo.lemma_names()[0])

			adjList=temp

		i=i+1

	for m in graph.nodes():
		for n in graph.nodes():
			if graph.has_edge(m,n)==False:
				graph.add_edge(m,n,weight=0)

	nx.draw(graph,pos=nx.random_layout(graph),with_labels=True, node_color='#ADD8E6', font_size=5, width=0.2, alpha=0.4)

	plt.savefig("RnWalk.png", dpi=1000)

	known = []
	splus = []
	sminus = []
	for seed in seedList:
		known.append(seed[0])
		if seed[1]==1:
			splus.append(seed[0])
		if seed[1]==-1:
			sminus.append(seed[0])

	unknown = []
	for w in graph.nodes():
		if w not in known:
			unknown.append(w)

	for w in unknown:
		avg_pos=0
		avg_neg=0
		k=1
		while k<=5:
			htime=hit2plus(w,splus,graph,0)
			avg_pos=avg_pos+htime
			k=k+1
		avg_pos=avg_pos/5

		k=1
		while k<=5:
			htime=hit2minus(w,sminus,graph,0)
			avg_neg=avg_neg+htime

		avg_neg=avg_neg/5

		if avg_pos>avg_neg:
			seedList.append([w,1])
		else:
			seedList.append([w,-1])

	# print(seedList)
