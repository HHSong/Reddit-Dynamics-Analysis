import pickle
import treeNode
import os
import processor as processor
import networkx as nx
import matplotlib.pyplot as plt
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

def get_data(files):
    if os.path.isfile('./Stats/grah_stats'):
        with open('./Stats/grah_stats', 'rb') as f:
            lst = pickle.load(f)
        return lst[0], lst[1], lst[2], lst[3]
    cluster_lst = []
    deg_assort_lst = []
    cat_assort_lst = []
    num_usr_lst = []
    for file in files:
        if not os.path.isfile('./Stats/' + file + '.graph'):
            G = toXGraph(file)
            with open('./Stats/' + file + '.graph', 'wb') as f:
                pickle.dump(G, f)
    for file in files:
        G = nx.Graph()
        with open('./Stats/' + file + '.graph', 'rb') as f:
            G = pickle.load(f)
        print(file + ' in progress...', flush=True)
        print(' ...calculating Clustering Coefficient...', flush=True)
        avg_clustering = nx.average_clustering(G, weight='weight')
        print(' ...calculating Degree Assortativity...', flush=True)
        deg_assortativity = nx.degree_assortativity_coefficient(G, weight='weight')
        print(' ...calculating Assortativity for Top Category...', flush=True)
        cat_assortativity = nx.attribute_assortativity_coefficient(G, 'category')
        print(' ...calculating Number of Unique Users...', flush=True)
        tmp_users = []
        for node in G.nodes():
            tmp_users.append(node)
        num_usr_lst.append(len(set(tmp_users)))
        cluster_lst.append(avg_clustering)
        deg_assort_lst.append(deg_assortativity)
        cat_assort_lst.append(cat_assortativity)
        print(' ... done', flush=True)
    with open('./Stats/grah_stats', 'wb') as f:
        pickle.dump([cluster_lst, deg_assort_lst, cat_assort_lst, num_usr_lst], f)  
    return cluster_lst, deg_assort_lst, cat_assort_lst, num_usr_lst
 
def plot_stats(files, cluster_lst, deg_assort_lst, cat_assort_lst, num_usr_lst):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(files, cluster_lst, color='#efdc4f', label='Average Clustering Coefficient')
    ax1.plot(files, deg_assort_lst, color='#ef9c4f', label='Degree Assortativity')
    ax1.plot(files, cat_assort_lst, color='#ef4f4f', label='Assortativity for Most Visited Subreddit')
    ax1.set_xlabel('snapshots')
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1), ncol=1)
    ax2.plot(files, num_usr_lst, color='#4a4b4c', label='Number of Users')
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 1), ncol=1)
    plt.title('Graph Statistics')
    plt.show()


if __name__ == '__main__':                    
    cluster_lst, deg_assort_lst, cat_assort_lst, num_usr_lst = get_data(files)
    plot_stats(files, cluster_lst, deg_assort_lst, cat_assort_lst, num_usr_lst)           
