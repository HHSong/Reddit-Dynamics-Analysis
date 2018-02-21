import treeNode
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import community
import movement_btw_snapshots as mov
import try_print as tprint
from networkx import bipartite

def tracker(filename):
    str = '&'
    new_str = str.replace('&', '\&')
    G=nx.Graph()
    with open (filename, 'r') as f:
        for line in  f:
            if line[0][0] == 'W' or line[0][0] == '-' or line[0][0] == 'B' or line[0][0] == '{' or line[0][0] == '}' or line[0][0] == new_str[0] or line == '\n': 
                pass
            else:
                newline = line.split('%')
                amount = newline[0]
                newline = newline[1].split()
                clustera = newline[2]
                clusterb = newline[6]
                G.add_node(clustera+'A', bipartite = 0,color = 'blue')
                G.add_node(clusterb+'B', bipartite = 1, color='red')
                G.add_weighted_edges_from([(clustera+'A',clusterb+'B',amount)])
    #l, r = nx.bipartite.sets(G)
 #   pos = {}
 #   pos.update((node, (1, index)) for index, node in enumerate(l))
 #   pos.update((node, (2, index)) for index, node in enumerate(r))
    node_color = []
    for node in G.nodes(data=True):
        if 'blue' in node[1]['color']:
            node_color.append('blue')
            
        else:
            node_color.append('red')
    pos = nx.circular_layout(G)
    nx.draw(G, pos=pos, with_labels=False, node_size=25, node_color=node_color)
    plt.show(G)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help = 'Specifies a particular input file to test')
    args = parser.parse_args()
    if args.file:
        filename = args.file
        tracker(filename)


if __name__ == '__main__':
    main()
