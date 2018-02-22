import treeNode
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import community
import movement_btw_snapshots as mov
import try_print as tprint

'''
Given a commandline file input of the snapshot, draws a graph of the communities
using louvain's algorithm
'''
def toXGraph(filename):
    G=nx.Graph()
    with open(os.path.join("output",filename), 'rb') as f:
        tmp_list = pickle.load(f)
        for i in range (0,len(tmp_list)):
            Master = tmp_list[i].getMaster()
            Slave = tmp_list[i].getSlave()
            Cat = tmp_list[i].getCat()
            G.add_weighted_edges_from([(Master,Slave,tmp_list[i].getWeight())])
            G.node[Master]['category'] = Cat
            G.node[Slave]['category'] = Cat

    partition = community.best_partition(G)
    #print(partition)
    '''
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
         count += 1.
         list_nodes = [nodes for nodes in partition.keys()
                        if partition[nodes] == com]
         nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))
         nx.draw_networkx_edges(G, pos, alpha=0.5)'''
    return partition
    #nx.draw(G)
 #   plt.show(G)
def compare(dict1,dict2):
    '''
 Takes in two partitions and returns the similar users in both clusters
'''
    d1 = set(dict1)
    d2 = set(dict2)
    G1=nx.Graph()
    for name in d1.intersection(d2):
        print(name,dict1[name],dict2[name])
 #       G1.add_edge(dict1[name],dict2[name])
    
 #   pos=nx.spring_layout(G1)
 #   nx.draw(G1)
 #   nx.draw_networkx_labels(G1,pos,font_size=5,font_family='sans-serif')
 #   plt.show(G1)

def common_user_percentage(first, second):
    """Takes in two partitions and returns the similar users in both clusters"""
    users1 = []
    for edge in first:
        users1.append(edge.master)
        users1.append(edge.slave)
    set1 = set(users1)
    users2 = []
    for edge in second:
        users2.append(edge.master)
        users2.append(edge.slave)
    set2 = set(users2)

    common = len(set1.intersection(set2))
    result = {
        'percentage':  common / len(set2),
        'common': common,
        'second': len(set2)
    }
    return result


def load(filename):
    filename = os.path.join(
        "../output",
        filename
    )
    fileObject = open(filename, 'rb')
    return pickle.load(fileObject)


def partition_stats():
    parts = [
        '2008-07.partition',
        '2008-11.partition',
        '2009-03.partition',
        '2009-07.partition',
        '2009-11.partition',
        '2010-03.partition',
        '2010-07.partition',
        '2010-11.partition',
        '2011-03.partition',
        '2011-07.partition',
        '2011-11.partition',
        '2012-03.partition',
        '2012-07.partition',
        '2012-11.partition'
    ]
    stats = {}
    data = []
    for partition in parts:
        data.append(load(partition))
    for i in range(len(parts)-1):
        stats[parts[i]] = common_user_percentage(data[i], data[i+1])

    for file, stat in stats.items():
        print(file, stat)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1','--file1',help = 'Specifies a particular input file to test')
    parser.add_argument('-f2','--file2',help = 'Specifies a particular input file to test')
    args = parser.parse_args()
    if args.file1 and args.file2:
        filename1 = args.file1
        filename2 = args.file2
        dict1 = toXGraph(filename1)
        dict2 = toXGraph(filename2)
        print(common_user_percentage(dict1,dict2))
 #       compare(dict1,dict2)
        output = mov.create_newdict(dict1,dict2)
        res = mov.percentage_of(output[0],len(output[1]),dict2)
 #       print(res)
        mov.print_old_to_new(res)
        res = mov.percentage_of(output[1],len(output[0]),dict1)
        mov.print_new_from_old(res)




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
