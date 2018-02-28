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
import string
from networkx import bipartite

'''
Produces a simple sankey graph showing cluster movement between two consecutive snapshots
Thresh indicates the threshold. Cluster movement below the threshold will not be
visualized. Thresh is a percentage, a float between 0 and 100
Input is a rtf file with the cluster movement percentages
'''
def track_sankey_low_pass(filename, thresh):
    new_str = '&'.replace('&', '\&')
    ids = {}
    id = 0
    labels = []
    sources = []
    targets = []
    values = []
    with open(filename, 'r') as f:
        f = strip_lines(f)
        for line in f:
            newline = line.split('%')
            amount = newline[0]
            if float(amount) > thresh:
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
    sankey.sankey(filename, sources, targets, values, labels, filename+"low-pass")


def strip_lines(f):
    out = []
    to_skip = True
    for line in f:
        if to_skip and "CocoaLigature0" not in line:
            continue
        if "CocoaLigature0" in line:
            to_skip = False
            i = line.index("CocoaLigature0")
            out.append(line[i + len("CocoaLigature0") + 2:])
            continue
        out.append(line)
    return out



def track_sankey_high_pass(filename, thresh):
    new_str = '&'.replace('&', '\&')
    ids = {}
    id = 0
    labels = []
    sources = []
    targets = []
    values = []
    with open(filename, 'r') as f:
        f = strip_lines(f)
        for line in f:
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
    sankey.sankey(filename, sources, targets, values, labels, filename+"high-pass")

'''
Main driver that constructs the sankey graph for the first four
snapshots. The graph shows the movement of the clusters from
snapshot to snapshot
'''
def overall_sankey():
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
    rtfs = []
    for letter in string.ascii_uppercase[:13]:
        rtfs.append(letter + ".rtf")
    new_str = '&'.replace('&', '\&')
    ids = {}
    id = 0
    labels = []
    sources = []
    targets = []
    values = []
    snapshots_per_graph = 3
    prev = None
    out = {}
    not_first = False
    next_out = {}
    # for i in range(len(rtfs)):
    for i in range(snapshots_per_graph):

        rtf = rtfs[i]
        inactive = "inactive" + "#" + parts[i][:7]
        ids[inactive] = id
        id += 1
        labels.append(inactive)
        # connect inactive
        if prev is not None:
            sources.append(ids[prev])
            targets.append(ids[inactive])
            values.append(1)

        # connect to inactive
        for key, ended in out.items():
            if not ended:
                sources.append(ids[key])
                targets.append(ids[inactive])
                values.append(1)
                out[key] = True
        out = next_out
        next_out = {}

        with open("Stats/" + rtf, 'r') as f:
            f = strip_lines(f)
            for line in f:
                newline = line.split('%')
                amount = newline[0]
                newline = newline[1].split()
                clustera = newline[2]
                clusterb = newline[6]
                # in
                in_key = clustera + '#' + parts[i][:7]
                if in_key not in ids:
                    ids[in_key] = id
                    id += 1
                    labels.append(in_key)
                    if not_first:
                        sources.append(ids[prev])
                        targets.append(ids[in_key])
                        values.append(1)
                if in_key in out:
                    out[in_key] = True

                # out
                out_key = clusterb + '#' + parts[i+1][:7]
                if out_key not in ids:
                    ids[out_key] = id
                    id += 1
                    labels.append(out_key)
                    if i != snapshots_per_graph-1:
                        next_out[out_key] = False

                sources.append(ids[in_key])
                targets.append(ids[out_key])
                values.append(amount)

        prev = inactive
        not_first = True

    # init last inactive sink
    inactive = "inactive" + "#" + parts[snapshots_per_graph][:7]
    ids[inactive] = id
    id += 1
    labels.append(inactive)
    sources.append(ids[prev])
    targets.append(ids[inactive])
    values.append(1)
    # connect
    for key, ended in out.items():
        if not ended:
            sources.append(ids[key])
            targets.append(ids[inactive])
            values.append(1)
            out[key] = True
    sankey.sankey("overall", sources, targets, values, labels, filename)


'''
Produces a simple sankey graph showing cluster movement between two consecutive snapshots
Input is a rtf file with the cluster movement percentages
'''
def track_sankey(filename):
    new_str = '&'.replace('&', '\&')
    ids = {}
    id = 0
    labels = []
    sources = []
    targets = []
    values = []
    with open(filename, 'r') as f:
        f = strip_lines(f)
        for line in f:
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
    sankey.sankey(filename, sources, targets, values, labels, filename)


'''
Takes a rtf file with the old cluster to new cluster stdout percentages and converts
to a bipartite graph, showing the older cluster moving to the new cluster
'''
def tracker(filename):
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

'''
Main function for testing graphical display. Reconfigure as necessary.
'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help = 'Specifies a particular input file to test')
    parser.add_argument('-t','--thresh',help = 'Specifies a particular threshold to test')
    args = parser.parse_args()
    if args.file:
        filename = args.file
        #track_sankey(filename)
        #tracker(filename)
        if args.thresh:
            thresh = float(args.thresh)
            # track_sankey_consolid(filename,thresh)


'''
uncomment main() to run functions in main(). Else, it generates the overall
sankey graph for the first 4 snapshots
'''
if __name__ == '__main__':
    main()
    # overall_sankey()
    # track_sankey("Stats/K.rtf")
    filename = "Stats/A.rtf"
    # track_sankey_high_pass(filename, 2)
    track_sankey_low_pass(filename, 40)