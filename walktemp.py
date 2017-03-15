import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

def Orntpred(seedList):		
							
	size1=len(seedList)			#Check length of seedlist before
	Orntsrch(seedList)
	size2=len(seedList)			#Check length of seedlist after
	print("m")
	if size2==size1:			#If none added to seedlist from adjective list, abort!
		return

def Orntsrch(seedList):
	x=0
	for x in range(10000):
		x=x+1
		if x>1:
			break
		print("Hello")
		i=0
		for seed in seedList:
			i=i+1
			if i>5:
				break
			print("inhere")
			synseed = []
			j=0
			for syn in wn.synsets(seed[0]):
				j=j+1
				if j>5:
					break
				synseed.append(syn.lemma_names()[0])

			anytseed=[]
			j=0
			for syn in wn.synsets(seed[0]):
				j=j+1
				if j>5:
					break
				l=syn.lemmas()[0]
				if l.antonyms():
					for anyt in l.antonyms():
						anytseed.append(anyt.name())

			hyprseed=[]
			j=0
			syn = wn.synsets(seed[0])
			for s in syn:
				j=j+1
				if j>5:
					break
				for hypr in s.hypernyms():
					hyprseed.append(hypr.lemma_names()[0])

			hyposeed=[]
			j=0
			syn = wn.synsets(seed[0])
			for s in syn:
				j=j+1
				if j>5:
					break				
				for hypo in s.hyponyms():
					hyposeed.append(hypo.lemma_names()[0])

			for a in synseed:
				add=[a,seed[1]]
				if a not in seedList:
					seedList.append(add)
					graph.add_node(a)
				graph.add_edge(seed[0],a)


			
			for a in anytseed:
				add=[a,-seed[1]]
				if a not in seedList:
					seedList.append(add)
					graph.add_node(a)
				graph.add_edge(seed[0],a)

			for a in hyprseed:
				add=[a,seed[1]]
				if a not in seedList:
					seedList.append(add)
					graph.add_node(a)
				graph.add_edge(seed[0],a)

			for a in hyposeed:
				add=[a,seed[1]]
				if a not in seedList:
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

	print('\nSeedList\n')
	print(seedList)
	print('\n')

	Orntpred(seedList)	#First function call

	print('\nSeedList\n')
	print(seedList)
	f=open('seeds_trained.txt','w')
	f.write(str(seedList))

	for seed in seedList:
		if seed[1]==1:
			posList.append(seed[0])
		elif seed[1]==-1:
			negList.append(seed[0])
		elif seed[1]==0:
			neutList.append(seed[0])
			

	nx.draw(graph, pos=nx.random_layout(graph), nodelist=posList, node_color='g', alpha=0.9, font_size=8, width=0.5, with_labels=True)

	nx.draw(graph, pos=nx.random_layout(graph), nodelist=negList, node_color='r', alpha=0.9, font_size=8, width=0.5, with_labels=True)

	nx.draw(graph, pos=nx.random_layout(graph), nodelist=neutList, node_color='b', alpha=0.9, font_size=8, width=0.2, with_labels=True)

	plt.savefig("walk4.png")






