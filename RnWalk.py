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
		wt=graph[i][nb]['weight']
		wtsum=wtsum+wt
	return graph[i][j]['weight']/wtsum

def hit2plus(i,splus,graph,count):
	if count<=2:
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
	else:
		return count

def hit2minus(i,sminus,graph,count):
	if count<=2:
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
	else:
		return count	

if __name__ == "__main__":

	seedList = [['good', 1],['bad', -1], ['Love', 1], ['hate', -1],['right',1],['wrong',-1]]
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
						graph.add_edge(a,anyt.name(),weight=0.1)
						temp.append(anyt.name())

			for hypr in syn.hypernyms():
				if hypr.lemma_names()[0] not in graph.nodes():
					graph.add_node(hypr.lemma_names()[0])	#hypernyms
					graph.add_edge(a,hypr.lemma_names()[0],weight=0.5)
					temp.append(hypr.lemma_names()[0])

			for hypo in syn.hyponyms():
				if hypo.lemma_names()[0] not in graph.nodes():
					graph.add_node(hypo.lemma_names()[0])	#hypornyms
					graph.add_edge(a,hypo.lemma_names()[0],weight=0.5)
					temp.append(hypo.lemma_names()[0])

			for mero in syn.part_meronyms():
				if mero.lemma_names()[0] not in graph.nodes():					
					graph.add_node(mero.lemma_names()[0]) 	#meronyms
					graph.add_edge(a,mero.lemma_names()[0],weight=0.5)
					temp.append(mero.lemma_names()[0])

			adjList=temp

		i=i+1

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
		pos_htime=0
		neg_htime=0
		k=1
		while k<=10:
			htime=hit2plus(w,splus,graph,0)
			pos_htime=pos_htime+htime
			k=k+1
		pos_htime=pos_htime/5

		k=1
		while k<=10:
			htime=hit2minus(w,sminus,graph,0)
			neg_htime=neg_htime+htime
			k=k+1
		neg_htime=neg_htime/5

		if pos_htime<neg_htime:
			seedList.append([w,1])
			splus.append(w)
		elif neg_htime<pos_htime:
			seedList.append([w,-1])
			sminus.append(w)
		else:
			seedList.append([w,0])

	print(seedList)
