import treeNode
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import community
import array
import movement_btw_snapshots as mov
import try_print as tprint
import sankey
from networkx import bipartite

def track_sankey_consolid(filename,thresh):
    new_str = '&'.replace('&', '\&')
    ids = {}
    id = 0
    labels = []
    sources = []
    targets = []
    values = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0][0] == 'W' or line[0][0] == '-' or line[0][0] == 'B' or line[0][0] == '{' \
                    or line[0][0] == '}' or line[0][0] == new_str[0] or line == '\n':
                pass
            else:
                newline = line.split('%')
                amount = newline[0]
                if float(amount) < thresh:
                    pass
                else:
                    amount = newline[0]
                    newline = newline[1].split()
                    clustera = newline[2]
                    clusterb = newline[6]
                    key = clustera + 'A'
                    if key not in ids:
                        ids[key] = id
                        id += 1
                        labels.append(key)
                    sources.append(ids[key])
                    key = clusterb + 'B'
                    if key not in ids:
                        ids[key] = id
                        id += 1
                        labels.append(key)
                    targets.append(ids[key])
                    values.append(amount)
    sankey.sankey(filename, sources, targets, values, labels)

    
def track_sankey(filename):
    new_str = '&'.replace('&', '\&')
    ids = {}
    id = 0
    labels = []
    sources = []
    targets = []
    values = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0][0] == 'W' or line[0][0] == '-' or line[0][0] == 'B' or line[0][0] == '{' \
                    or line[0][0] == '}' or line[0][0] == new_str[0] or line == '\n':
                pass
            else:
                newline = line.split('%')
                amount = newline[0]
                newline = newline[1].split()
                clustera = newline[2]
                clusterb = newline[6]
                key = clustera + 'A'
                if key not in ids:
                    ids[key] = id
                    id += 1
                    labels.append(key)
                sources.append(ids[key])
                key = clusterb + 'B'
                if key not in ids:
                    ids[key] = id
                    id += 1
                    labels.append(key)
                targets.append(ids[key])
                values.append(amount)
    sankey.sankey(filename, sources, targets, values, labels)


def tracker(filename):
    '''
Takes a rtf file with the old cluster to new cluster stdout percentages adn converts to a bipartite graph
'''
    str = '&'
    new_str = str.replace('&', '\&')
    G=nx.Graph()
    with open (filename, 'r') as f:
        for line in  f:
            if line[0][0] == 'W' or line[0][0] == '-' or line[0][0] == 'B' or line[0][0] == '{' \
                    or line[0][0] == '}' or line[0][0] == new_str[0] or line == '\n':
                pass
            else:
                newline = line.split('%')
                amount = newline[0]
                newline = newline[1].split()
                clustera = newline[2]
                clusterb = newline[6]
                G.add_node(clustera+'A', bipartite = 0, color='blue')
                G.add_node(clusterb+'B', bipartite = 1, color='red')
                G.add_weighted_edges_from([(clustera+'A',clusterb+'B',amount)])
    node_color = []
    pos = {}
    numBlue = 0
    numRed = 0
    yBlue = 0.01
    yRed = 0.01
    for node in G.nodes(data=True):
        if 'blue' in node[1]['color']:
            node_color.append('blue')
            numBlue += 1
        else:
            node_color.append('red')
            numRed += 1
    yDistBlue : float = 2.0 / numBlue
    yDistRed : float = 2.0 / numRed

    ax = plt.axes()
    ax.set_axis_off()

    for node in G.nodes(data=True):
        if node[1]['color'] == 'blue':
            pos[node[0]] = array.array('f', [0, yBlue])
            yBlue += yDistBlue
        else:
            pos[node[0]] = array.array('f', [1, yRed])
            yRed += yDistRed

    nx.draw(G, pos=pos, with_labels=False, node_size=25, node_color=node_color, ax=ax)


def pie(ax, center):
    # ax = plt.axes()
    # fig1, ax1 = plt.subplots()
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)
    ax.pie(sizes,
           # autopct='%1.1f%%',
           # shadow=True,
           startangle=90, radius=0.15, center=center)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help = 'Specifies a particular input file to test')
    args = parser.parse_args()
    if args.file:
        filename = args.file
        track_sankey(filename)
#        track_sankey_consolid(filename,thresh)
        # tracker(filename)

if __name__ == '__main__':
    main()
