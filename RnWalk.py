import nltk
from nltk.corpus import wordnet as wn
from nltk import pos_tag,word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
from textblob import Word
from random import choice
import numpy as np


def tag2letter(word):
	#print('here')
	t=pos_tag(word_tokenize(word))
	if t[0][1]=='JJ':
		return 'a'
	elif t[0][1]=='NN':
		return 'n'
	elif t[0][1]=='VB':
		return 'v'
	else:
		return '1'


def transit_P (i,j,graph):
	nbrs=graph.neighbors(i)
	wtsum=0
	for nb in nbrs:
		wt=graph[i][nb]['weight']
		wtsum=wtsum+wt
	return graph[i][j]['weight']/wtsum

def hit2plus(i,splus,graph,count):
	if count<=5:
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
	if count<=5:
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
	while i<=2:
		temp = []	
		for a in adjList:			
			for syn in wn.synsets(a):				#synonyms
				word=syn.lemma_names()[0]
				if word not in graph.nodes():
					graph.add_node(word)
					word1=wn.synset(a[0]+'.n.01')
					word2=wn.synset(word[0]+'.n.01')
					w=wn.path_similarity(word1,word2)
					graph.add_edge(a,word,weight=w)
					temp.append(word)

			syn=Word(a).synsets[0]

			l=syn.lemmas()[0]
			if l.antonyms():
				for anyt in l.antonyms():
					if anyt.name() not in graph.nodes():		
						graph.add_node(anyt.name())		#antonyms
						
						temp.append(anyt.name())
						#print('------------------------------------')
						#print(anyt.name())				
						#print('------------------------------------')
						#wtag=pos_tag(word_tokenize(anyt.name()))
						#wn_tag=penn_to_wn(wtag)
						#lemma = lemmatzr.lemmatize(wtag[0], pos=wn_tag)
						#word2=wn.synsets(lemma,pos=wn_tag)
						tg=tag2letter(anyt.name())
						#print('back')
						if tg=='1':
							continue
						word1=wn.synset(a[0]+'.n.01')
						try:
							word2=wn.synset(anyt.name()+'.'+tg+'.01')
						except:
							graph.add_edge(a,anyt.name(),weight=0.1)
							continue
						else:
						#word2=wn.synset(word2)
							w=wn.path_similarity(word1,word2)						
							graph.add_edge(a,anyt.name(),weight=w)


			for hypr in syn.hypernyms():
				if hypr.lemma_names()[0] not in graph.nodes():

					word1=wn.synset(a[0]+'.n.01')
					#print('------------------------------------')
					#print(hypr.lemma_names()[0])
					#print('------------------------------------')
					#temp1=hypr.lemma_names()[0]
					tg=tag2letter(hypr.lemma_names()[0])
					graph.add_node(hypr.lemma_names()[0])
					temp.append(hypr.lemma_names()[0])

					if tg==1:
						continue
					word1=wn.synset(a[0]+'.n.01')
					try:
						word2=wn.synset(hypr.lemma_names()[0]+'.'+tg+'.01')
					except:
						graph.add_edge(a,hypr.lemma_names()[0],weight=0.3)
						continue
					else:
						w=wn.path_similarity(word1,word2)
						graph.add_edge(a,hypr.lemma_names()[0],weight=w)
					#word2=wn.synset(temp1)
					
					#w=wn.path_similarity(word1,word2)
						#hypernyms
					
					

			for hypo in syn.hyponyms():
				if hypo.lemma_names()[0] not in graph.nodes():					
					graph.add_node(hypo.lemma_names()[0]) 	#hyponyms
					temp.append(hypo.lemma_names()[0])

					tg=tag2letter(hypo.lemma_names()[0])

					if tg==1:
						continue

					word1=wn.synset(a[0]+'.n.01')
					try:
						word2=wn.synset(hypo.lemma_names()[0]+'.'+tg+'.01')
					except:
						graph.add_edge(a,hypo.lemma_names()[0],weight=0.5)
						continue
					else:
						w=wn.path_similarity(word1,word2);
						graph.add_edge(a,hypo.lemma_names()[0],weight=w)

			adjList=temp

		i=i+1

	nx.draw(graph,pos=nx.random_layout(graph),with_labels=True, node_color='#ADD8E6', font_size=5, width=0.2, alpha=0.4)

	plt.savefig("RnWalk2.png", dpi=1000)

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
		while k<=5:
			htime=hit2plus(w,splus,graph,0)
			pos_htime=pos_htime+htime
			k=k+1
		pos_htime=pos_htime/5

		k=1
		while k<=5:
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
