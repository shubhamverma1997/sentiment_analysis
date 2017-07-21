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

    acceptedRelations=[]
    acceptedRelations.append('IsA')
    acceptedRelations.append('CapableOf')
    acceptedRelations.append('UsedFor')
    acceptedRelations.append('FormOf')
    acceptedRelations.append('RelatedTo')
    acceptedRelations.append('Causes')
    acceptedRelations.append('HasProperty')
    acceptedRelations.append('Synonym')
    acceptedRelations.append('Antonym')
    
    seedList = [['good', 1],['bad', -1], ['Love', 1], ['hate', -1],['right',1],['wrong',-1]]
    known=[]
    splus=[]
    sminus=[]
    temp=[]
    for seed in seedList:
        known.append(seed[0])
        temp.append(seed[0])
        if seed[1]>0:
            splus.append(seed[0])
        if seed[1]<0:
            sminus.append(seed[0])
    graph=nx.Graph()
            
    
    
    for k in known:
        graph.add_node(k)

    i=1
    while i<=2:
        addedwords=[]
        for k in known:
            counter=0
            obj=requests.get('http://api.conceptnet.io/c/en/'+k+'?filter=/c/en').json()
            related=obj['edges']


            for re in related:
                end=re['end']
                start=re['start']
                if counter>10:
                    break
                word=end['label']
                if word not in addedwords:
                    r=re['rel']
                    if r['label'] in acceptedRelations:
                        addedwords.append(word)
                        graph.add_node(word)
                
                newword=str(word)
                graph.add_edge(k,newword,weight=re['weight'])
                counter=counter+1   

                word=start['label']
                if word not in addedwords:
                    r=re['rel']
                    if r['label'] in acceptedRelations:
                        addedwords.append(word)
                        graph.add_node(word)
                newword=str(word)
                graph.add_edge(k,newword,weight=re['weight'])
                counter=counter+1   
        known=addedwords
        i=i+1
    nx.draw(graph,pos=nx.random_layout(graph),with_labels=True, node_color='#ADD8E6', font_size=5, width=0.2, alpha=0.4)
    plt.savefig("RnWalkCN.png", dpi=400)

    unknown=[]
    for w in graph.nodes():
        if w not in temp:
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
            seedList.append([w,round(1/pos_time,2)])
            splus.append(w)

        elif neg_time<pos_time:
            seedList.append([w,round(-1/neg_time,2)])
            sminus.append(w)
        else:
            seedList.append([w,0])

    print(seedList)
