import pickle
import treeNode
import os
import processor as processor
import networkx as nx
import matplotlib.pyplot as plt
import json
import constants
import rtf_broker
import numpy
import sankey
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
        for i in range(0, len(tmp_list)):
            Master = tmp_list[i].getMaster()['id']
            Slave = tmp_list[i].getSlave()['id']
            CatM = tmp_list[i].getMaster()['categories']
            CatS = tmp_list[i].getSlave()['categories']
            G.add_weighted_edges_from([(Master, Slave, tmp_list[i].getWeight())])
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


def category_distribution_per_flow():
    snapshot_category_dict = json.load(open("Stats/snapshot_category_dict.json"))
    rfts = [
        "Stats/" + file for file in rtf_broker.rtf_files()
    ]
    distributions = []
    for i in range(len(constants.parts) - 1):
        snapshotA = constants.parts[i]
        snapshotB = constants.parts[i + 1]
        rtf_file = rfts[i]
        categoriesA = snapshot_category_dict[snapshotA]
        categoriesB = snapshot_category_dict[snapshotB]
        distribution = {}  # {1: [same, volume]}
        movements = rtf_broker.movements(rtf_file)
        for move in rtf_broker.movements(rtf_file):
            a = int(move[0])
            b = int(move[1])
            if a >= len(categoriesA) or b >= len(categoriesB):
                continue
            catA = categoriesA[a][0][0]
            if len(categoriesB[b]) == 0:
                print(rtf_file)
            catB = categoriesB[b][0][0]
            percentage = move[2]
            array = distribution.get(a, [0, 0])
            if catA == catB:
                array[0] += percentage
            array[1] += percentage
            distribution[a] = array
        data = []
        for cluster, array in distribution.items():
            same = array[0]
            volume = array[1]
            data.append(
                 float(same / volume) * 100
            )
        data = collect(data, 50)
        distributions.append(data)
    return numpy.arange(0, 100, 100 / 50), distributions


def collect(array, bands):
    total = len(array)
    data = numpy.zeros(
        bands,
        dtype=int
    )

    step = 100 / bands
    for number in array:
        index = int(number / step)
        if index == len(data):
            index -= 1
        data[index] += 1
    data = [
        d / total * 100 for d in data
    ]
    return data


if __name__ == '__main__':
    # cluster_lst, deg_assort_lst, cat_assort_lst = get_data(files)
    # plot_stats(files, cluster_lst, deg_assort_lst, cat_assort_lst)

    rfts = [
        "Stats/" + file for file in rtf_broker.rtf_files()
    ]
    # print(rfts[10])
    x, ys = category_distribution_per_flow()
    for i in range(len(ys)):
        filename = rfts[i].rsplit('.', 1)[0] + '_distribution.html'
        timeA = constants.parts[i].rsplit('.', 1)[0]
        timeB = constants.parts[i + 1].rsplit('.', 1)[0]
        title = timeA + " to " + timeB + " interest continuity"
        sankey.bar(x, ys[i], filename, title)
