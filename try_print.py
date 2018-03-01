import treeNode
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import community
import processor
import json
from collections import Counter
import numpy as np

'''
Given filename of the snapshot (a partition file), runs louvain's
algorithm to separate the snapshot into communities. Returns
the communities. Uncomment the commented out code below to draw
the communities/clusters of snapshot. The graph is drawn using
Networkx
'''
def toXGraph(filename):
    G=nx.Graph()
    with open(os.path.join("output",filename), 'rb') as f:
        tmp_list = pickle.load(f)
        tmp_list = processor.aggregate_edges(tmp_list)
        for i in range (0,len(tmp_list)):
            Master = tmp_list[i].getMaster()['id']
            Slave = tmp_list[i].getSlave()['id']
            CatM = tmp_list[i].getMaster()['categories']
            CatS = tmp_list[i].getSlave()['categories']
            G.add_weighted_edges_from([(Master,Slave,tmp_list[i].getWeight())])
            G.node[Master]['category'] = CatM
            G.node[Slave]['category'] = CatS
    partition = community.best_partition(G)
    '''
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
        count += 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = str(count / size))
        nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show(G)
    '''
    return (partition,G)


'''
Given the communitites returned by louvain's algorithm of a snapshot (partition return from
toXGraph function), finds number of clusters in graph
'''
def numCluster(partition):
    count = 0
    for each in partition:
        if partition[each] > count:
            count = partition[each]
    return count + 1


'''
Given return values from toXGraph, finds the categories for each cluster in a snapshot
and prints out the unique categories and the number of occurences of that category for each
structure. Also prints total number of users.
'''   
def getCategory(partition,G):
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
    for i in range (0, numClust):
        for each in uniq[i]:
            Total += categories[i].count(each)
            Val[i].append((each, categories[i].count(each)))
    for i in range(0, numClust):
        Val[i] = sorted(Val[i], key=lambda x: x[1], reverse=True)
        print("cluster", i, ": ", Val[i])


def getAggregateCats(partition, G, filename):
    '''
    Finds the top categories for each snapshot
    '''
    categories = []
    for each in partition:
        categories += G.node[each]['category']
    c = Counter(categories)
    cat_count = c.most_common()
    total = sum(c.values())
    cat_percentage = [(cat, count / total) for (cat, count) in cat_count]
    dict_c = {}
    dict_c['count'] = cat_count
    dict_c['percentage'] = cat_percentage
    dict_c['total'] = numCluster(partition) - 1
    if not os.path.isfile('./Stats/' + filename[:7] + '.lists'):
        with open('./Stats/' + filename[:7] + '.lists', 'wb') as f:
            pickle.dump(dict_c, f)
    for (cat, count) in cat_count:
        print(cat + ',{0:d},{1:.2f}%'.format(count, count / total * 100))


def getAvgCat(partition,G):
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
    for i in range (0, numClust):
        for each in uniq[i]:
            Total += categories[i].count(each)
            Val[i].append((each, categories[i].count(each)))
   # for i in range(0, numClust):
 #       Val[i] = sorted(Val[i], key=lambda x: x[1], reverse=True)
 #       print("cluster", i, ": ", Val[i])
    array = []
    for each in Val:
        array.append(len(each))

    n_array = np.array(array)
    print("mean: ",n_array.mean())
    print("std: ",n_array.std())
    print("min: ",n_array.min())
    print("max: ",n_array.max())
    
'''
Main Function to run tests. Reconfigure as appropriate
'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help = 'Specifies a particular input file to test')
    args = parser.parse_args()
    if args.file:
        filename = args.file                     
        capture = toXGraph(filename)
        partition = capture[0]
        #print(partition)
        G = capture[1]
 #       getCategory(partition,G)
 #       getAggregateCats(partition, G, filename)
        getAvgCat(partition,G)

        
if __name__ == '__main__':
    #main()

    print("2008-07.partition")
    capture = toXGraph("2008-07.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2008-11.partition")
    capture = toXGraph("2008-11.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2009-03.partition")
    capture = toXGraph("2009-03.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2009-07.partition")
    capture = toXGraph("2009-07.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2009-11.partition")
    capture = toXGraph("2009-11.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2010-03.partition")
    capture = toXGraph("2010-03.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2010-07.partition")
    capture = toXGraph("2010-07.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2010-11.partition")
    capture = toXGraph("2010-11.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2011-03.partition")
    capture = toXGraph("2011-03.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2011-07.partition")
    capture = toXGraph("2011-07.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2011-11.partition")
    capture = toXGraph("2011-11.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2012-03.partition")
    capture = toXGraph("2012-03.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2012-07.partition")
    capture = toXGraph("2012-07.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    print("2012-11.partition")
    capture = toXGraph("2012-11.partition")
    partition = capture[0]
    G = capture[1]
    getAvgCat(partition,G)
    



