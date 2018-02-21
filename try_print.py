import treeNode
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import community
import processor


'''
Given a commandline file input of the snapshot, draws a graph of the communities
using louvain's algorithm
'''
def toXGraph(filename):
    G=nx.Graph()
    with open(os.path.join("output",filename), 'rb') as f:
        tmp_list = pickle.load(f)
        tmp_list = processor.aggregate_edges(tmp_list)
        #print(tmp_list)
        for i in range (0,len(tmp_list)):
            Master = tmp_list[i].getMaster()['id']
            Slave = tmp_list[i].getSlave()['id']
            CatM = tmp_list[i].getMaster()['categories']
            CatS = tmp_list[i].getSlave()['categories']
            G.add_weighted_edges_from([(Master,Slave,tmp_list[i].getWeight())])
            G.node[Master]['category'] = CatM
            G.node[Slave]['category'] = CatS

    partition = community.best_partition(G)
    #print(partition)
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
         count += 1.
         list_nodes = [nodes for nodes in partition.keys()
                        if partition[nodes] == com]
         nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))
         nx.draw_networkx_edges(G, pos, alpha=0.5)
 #   nx.draw(G)
 #   plt.show(G)
    return (partition,G)
def numCluster(partition):
    '''
finds number of clusters in graph
'''
    count = 0
    for each in partition:
        if partition[each] > count:
            count = partition[each]

    #print(count)
    return count + 1
    
def getCategory(partition,cluster,G):
    '''
Finds the categories for each cluster and prints out the uniq categories and the number of occurences
of that category for each structure. Also prints total number o fusers
'''
    numClust = numCluster(partition)
    categories = [[] for i in range(numClust)]
    uniq = []
    for each in partition:
        categories[partition[each]].append(G.node[each]['category'])
    for i in range (numClust):
        flat_list = [item for category in categories[i] for item in category]
        categories[i] = flat_list
        uniq.append(set(categories[i]))
    Total = 0
    Val = [[] for i in range(numClust)]
    for i in range (0,numClust):
        for each in uniq[i]:
            Total += categories[i].count(each)
            Val[i].append((each, categories[i].count(each)))
    for i in range(0,numClust):
        Val[i] = sorted(Val[i],key=lambda x: x[1],reverse=True)
        print("cluster", i, ": ", Val[i])
    return Val
def getTotal(partition):
    count = 0
    for each in partition:
        count+=1
    print("Total Users:",count)
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help = 'Specifies a particular input file to test')
    args = parser.parse_args()
    if args.file:
        filename = args.file                     
        capture = toXGraph(filename)
        partition = capture[0]
        G = capture[1]
        getCategory(partition,1,G)
        getTotal(partition)

if __name__ == '__main__':
    main()
'''
G=nx.Graph()
G.add_node("hi")
G.add_node("bye")
G.add_nodes_from(["hi","bye",])
G.add_edge('a','b',weight=0.6)
G.add_nodes_from(["eat","cheese"])
G.add_nodes_from([4,1])
G.add_weighted_edges_from([(1,2,1),(1,3,0.75),(2,4,10),(3,4,0.375)])
elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos,node_size=700)
nx.draw_networkx_edges(G,pos,edgelist=elarge,
                    width=6)
nx.draw_networkx_edges(G,pos,edgelist=esmall,
                    width=6,alpha=0.5,edge_color='b',style='dashed')
nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
plt.show(G)
'''
