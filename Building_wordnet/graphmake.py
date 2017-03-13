import nltk
import networkx as nx
import matplotlib.pyplot as plt
f=open('review1.txt')
raw=f.read
#words=nltk.word_tokenize(raw)

graph=nx.Graph()
graph.add_node(2)
graph.add_node(3)
graph.add_node(4)
graph.add_node(5)
nx.draw(graph,pos=nx.spring_layout(graph))
plt.savefig("ra.png")