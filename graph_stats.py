import pickle
import treeNode
import os
import processor as processor
import networkx as nx
import matplotlib.pyplot as plt
import json
import constants
import rtf_broker
from collections import Counter

files = ['2008-07', '2008-11', '2009-03', '2009-07', '2009-11', '2010-03', 
         '2010-07', '2011-03', '2011-07', '2011-11', '2012-03', '2012-07', 
         '2012-11']

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

def toXGraph(filename):
    G = nx.Graph()
    with open('./output/' + filename + '.partition', 'rb') as f:
        tmp_list = pickle.load(f)
        tmp_list = processor.aggregate_edges(tmp_list)
        for i in range (0,len(tmp_list)):
            Master = tmp_list[i].getMaster()['id']
            Slave = tmp_list[i].getSlave()['id']
            CatM = tmp_list[i].getMaster()['categories']
            CatS = tmp_list[i].getSlave()['categories']
            G.add_weighted_edges_from([(Master,Slave,tmp_list[i].getWeight())])
            G.node[Master]['category'] = Most_Common(CatM)
            G.node[Slave]['category'] = Most_Common(CatS)
    return G


'''

'''
def get_data(files):
    cluster_lst = []
    deg_assort_lst = []
    cat_assort_lst = []
    for file in files:
        if not os.path.isfile('./Stats/' + file + '.graph'):
            G = toXGraph(file)
            with open('./Stats/' + file + '.graph', 'wb') as f:
                pickle.dump(G, f)
    for file in files:
        G = nx.Graph()
        with open('./Stats/' + file + '.graph', 'rb') as f:
            G = pickle.load(f)
        print(file + ' in progress...', end='', flush=True)
        avg_clustering = nx.average_clustering(G, weight='weight')
        deg_assortativity = nx.degree_assortativity_coefficient(G, weight='weight')
        cat_assortativity = nx.attribute_assortativity_coefficient(G, 'category')
        print('done', flush=True)
        cluster_lst.append(avg_clustering)
        deg_assort_lst.append(deg_assortativity)
        cat_assort_lst.append(cat_assortativity)
    return cluster_lst, deg_assort_lst, cat_assort_lst
 
def plot_stats(files, cluster_lst, deg_assort_lst, cat_assort_lst):
    plt.plot(files, cluster_lst, color='#efdc4f', label='Average Clustering Coefficient')
    plt.plot(files, deg_assort_lst, color='#ef9c4f', label='Degree Assortativity')
    plt.plot(files, cat_assort_lst, color='#ef4f4f', label='Assortativity for Most Visited Subreddit')
    plt.xlabel('snapshots')
    plt.legend(loc='best', bbox_to_anchor=(1, 1), ncol=1)
    plt.title('Graph Statistics')
    plt.show()


def category_distribution():
    snapshot_category_dict = json.load(open("Stats/snapshot_category_dict.json"))
    rfts = [
        "Stats/" + file for file in rtf_broker.rtf_files()
    ]
    for i in range(len(constants.parts)):
        snapshotA = constants.parts[i]
        snapshotB = constants.parts[i+1]
        rtf_file = rfts[i]
        categoriesA = snapshot_category_dict[snapshotA]
        categoriesB = snapshot_category_dict[snapshotB]
        distribution = []
        for move in rtf_broker.movements(rtf_file):
            a = int(move[0])
            b = int(move[1])
            catA = categoriesA[a][0][0]
            catB = categoriesB[b][0][0]
            percentage = move[2]
            print(catA + " " + catB)
            # if catA == catB:
                # distribution.append(percentage)
        print(distribution)
        break


if __name__ == '__main__':                    
    # cluster_lst, deg_assort_lst, cat_assort_lst = get_data(files)
    # plot_stats(files, cluster_lst, deg_assort_lst, cat_assort_lst)
    category_distribution()