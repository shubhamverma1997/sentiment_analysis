import requests
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def transit_P(i,j,graph):
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
            probs=[]
            for j in graph.neighbors(i):
                probs.append(transit_P(i,j,graph))
            draw=np.random.choice(graph.neighbors(i),p=probs)
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
            probs=[]
            for j in graph.neighbors(i):
                probs.append(transit_P(i,j,graph))
            draw=np.random.choice(graph.neighbors(i),p=probs)
            return hit2minus(draw,sminus,graph,count+1)

    else:
        return count
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
            if counter>10:
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

    known=[]
    splus=[]
    sminus=[]
    for seed in seedList:
        known.append(seed[0])
        if seed[1]==1:
            splus.append(seed[0])
        if seed[1]==-1:
            sminus.append(seed[0])


    unknown=[]
    for w in graph.nodes():
        if w not in known:
            unknown.append(w)

    for w in unknown:
        pos_time=0
        neg_time=0
        k=1
        while k<=10:
            htime=hit2plus(w,splus,graph,0)
            pos_time=pos_time+htime
            k=k+1
        pos_time=pos_time/5

        k=1
        while k<=10:
            htime=hit2minus(w,sminus,graph,0)
            neg_time=neg_time+htime
            k=k+1
        neg_time=neg_time/5

        if pos_time<neg_time:
            seedList.append([w,1])
            splus.append(w)

        elif neg_time<pos_time:
            seedList.append([w,-1])
            sminus.append(w)
        else:
            seedList.append([w,0])

    print(seedList)
#original name cn.py