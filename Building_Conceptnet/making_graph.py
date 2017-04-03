import requests
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    seedList = [['good', 1],['bad', -1], ['Love', 1], ['hate', -1],['right',1],['wrong',-1]]
    addedwords=[]
    graph=nx.Graph()
    for seed in seedList:
        graph.add_node(seed[0])
    for seed in seedList:
        counter=0
        obj=requests.get('http://api.conceptnet.io/related/c/en/'+seed[0]+'?filter=/c/en').json()
        print('\n')
        related=obj['related']
        for re in related:
            if counter>5:
                break
            word=re['@id']
            print(word[6:]+'\t')
            if word[6:] not in addedwords:
                addedwords.append(word[6:])
                graph.add_node(word[6:])
            newword=str(word[6:])
            graph.add_edge(seed[0],newword,weight=re['weight'])
            counter=counter+1
        print('\n')
    nx.draw(graph,pos=nx.circular_layout(graph),with_labels=True, node_color='#ADD8E6', font_size=5, width=0.2, alpha=0.4)
    labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph,pos=nx.circular_layout(graph),edge_labels=labels)

    plt.savefig("RnWalk2.png", dpi=1000)

    print(addedwords)
#original name cn.py
