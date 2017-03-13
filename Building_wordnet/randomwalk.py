import networkx as nx
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn
from textblob import Word

f = open('Words.txt')
raw = f.read()
words=nltk.word_tokenize(raw)

#print(words)
f=open('seed_words.txt')
raw = f.read()
seeds=nltk.word_tokenize(raw)

score=open('seed_words.txt').read()
print(score)
setofwords=words+seeds

graph=nx.Graph()
i=1
j=1
flag=0
for word in setofwords:
	if j>=6:
		if flag==0:
			j=2
			flag=1
		elif flag==1:
			j=1
			flag=0
		i=i+1
	graph.add_node(word,pos=(i,j))
	j=j+2

for word1 in setofwords:
	if Word(word1).synsets:
		w1=Word(word1).synsets[0]
		for word2 in setofwords:
			if Word(word2).synsets:
				w2=Word(word2).synsets[0]
				wt=w1.wup_similarity(w2)
				if wt!=None and wt>0.3 and wt!=1:
					graph.add_edge(word1,word2,weight=round(wt,2))			
pos=nx.get_node_attributes(graph,'pos')
#nx.draw(graph, pos, node_color='b', alpha=0.8, font_size=7.5, width=1, with_labels=True)
labels=nx.get_edge_attributes(graph,'weight')
#nx.draw_networkx_edge_labels(graph,pos,alpha=0.7,edge_labels=labels,font_size=6)

#plt.savefig("randomwalk.png")

wt=0;
word="S"
flag=0
for w in graph.nodes():
	print("\n")
	wt=0
	flag=0
	if Word(w).synsets:
		w1=Word(w).synsets[0]
	for s in score.split():
		#print(1)
		if Word(s).synsets:
			w2=Word(s).synsets[0]
			if(w1.wup_similarity(w2)>wt):
				wt=w1.wup_similarity(w2)
				word=s
	
	if ord(word[0])>=65 and ord(word[0])<=90:
		print("inside")
		print(w)
		print(word)
		labels=nx.get_edge_attributes(graph,'weight')
		nx.draw(graph,pos=nx.circular_layout(graph),nodelist=[w],node_color='g',with_labels=True)
		#labels=nx.get_edge_attributes(graph,nodelist=[w],'weight')
		#pos=nx.get_node_attributes(graph,'pos')
		#nx.draw_networkx_edge_labels(graph,pos,alpha=0.7,edge_labels=labels,font_size=6)

	else:
		print("here")
		print(w)
		print(word)
		nx.draw(graph,pos=nx.circular_layout(graph),nodelist=[w],node_color='r',with_labels=True)
		#labels=nx.get_edge_attributes(graph,'weight')
		#pos=nx.get_node_attributes(graph,'pos')
		#nx.draw_networkx_edge_labels(graph,pos,alpha=0.7,edge_labels=labels,font_size=6)


#nx.draw_networkx_edges(graph,pos,alpha=0.7,edge_labels=labels,font_size=6)

plt.savefig("randomw.png")

