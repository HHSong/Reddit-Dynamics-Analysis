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
import numpy as np
from constants import parts
import rtf_broker
from rtf_broker import strip_lines, to_index


'''
Produces a simple sankey graph showing cluster movement between two consecutive snapshots
Thresh indicates the threshold. Cluster movement below the threshold will not be
visualized. Thresh is a percentage, a float between 0 and 100
Input is a rtf file with the cluster movement percentages
'''
def track_sankey_low_pass(filename, thresh):
    track_sankey(filename, passing=lambda amount: amount <= thresh, output=filename+"low-pass")


def track_sankey_high_pass(filename, thresh):
    track_sankey(filename, passing=lambda amount: amount >= thresh, output=filename + "high-pass")


'''
Main driver that constructs the sankey graph for the first four
snapshots. The graph shows the movement of the clusters from
snapshot to snapshot
'''
def overall_sankey():
    rtfs = rtf_broker.rtf_files()
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
    for i in range(snapshots_per_graph):
        rtf = rtfs[i]
        inactive = "inactive" + "#" + parts[i][:7]
        id = id_check(inactive, ids, id, labels)
        # connect inactive
        if prev is not None:
            create_flow(prev, inactive, 1, sources, targets, values, ids)

        # connect to inactive
        for key, ended in out.items():
            if not ended:
                create_flow(key, inactive, 1, sources, targets, values, ids)
                out[key] = True
        out = next_out
        next_out = {}

        for move in rtf_broker.movements("Stats/" + rtf):
            clustera = move[0]
            clusterb = move[1]
            amount = move[2]
            # in
            in_key = clustera + '#' + parts[i][:7]
            if in_key not in ids:
                id = id_check(in_key, ids, id, labels)
                if not_first:
                    create_flow(prev, in_key, 1, sources, targets, values, ids)
            if in_key in out:
                out[in_key] = True

            # out
            out_key = clusterb + '#' + parts[i+1][:7]
            if out_key not in ids:
                id = id_check(out_key, ids, id, labels)
                if i != snapshots_per_graph-1:
                    next_out[out_key] = False

            create_flow(in_key, out_key, amount, sources, targets, values, ids)

        prev = inactive
        not_first = True

    # init last inactive sink
    inactive = "inactive" + "#" + parts[snapshots_per_graph][:7]
    id = id_check(inactive, ids, id, labels)
    create_flow(prev, inactive, 1, sources, targets, values, ids)
    # connect
    for key, ended in out.items():
        if not ended:
            create_flow(key, inactive, 1, sources, targets, values, ids)
            out[key] = True
    sankey.sankey("overall", sources, targets, values, labels, filename)


'''
Produces a simple sankey graph showing cluster movement between two consecutive snapshots
Input is a rtf file with the cluster movement percentages
'''
def track_sankey(filename, passing=lambda amount: True, output=None):
    ids = {}
    labels = []
    sources = []
    targets = []
    values = []
    current_key = -1
    volume = 0
    file_index = to_index(filename)
    inactive = "inactive" + "#" + parts[file_index + 1][:7]
    id = id_check(inactive, ids, 0, labels)
    for move in rtf_broker.movements(filename):
        clustera = move[0]
        clusterb = move[1]
        amount = move[2]
        if not passing(amount):
            continue
        # in
        in_key = clustera + '#' + parts[file_index][:7]

        # volume control
        if current_key == in_key:
            volume -= amount
        else:
            if volume > 0:
                # draw sink
                create_flow(current_key, inactive, volume, sources, targets, values, ids)
            current_key = in_key
            volume = 100 - amount

        # out
        out_key = clusterb + '#' + parts[file_index + 1][:7]
        id = id_check(in_key, ids, id, labels)
        id = id_check(out_key, ids, id, labels)
        create_flow(in_key, out_key, amount, sources, targets, values, ids)

    if volume > 0:
        # draw sink
        create_flow(current_key, inactive, volume, sources, targets, values, ids)
    if output is None:
        name = parts[file_index][:7] + " to " + parts[file_index + 1][:7]
    else:
        name = filename
    return sankey.sankey(name, sources, targets, values, labels, name)

'''
creates flow for sankey grph
'''
def create_flow(in_key, out_key, amount, sources, targets, values, ids):
    sources.append(ids[in_key])
    targets.append(ids[out_key])
    values.append(amount)

'''
Checks for inactive users between snapshots
'''
def id_check(key, ids, id, labels):
    if key not in ids:
        ids[key] = id
        id += 1
        labels.append(key)
    return id

'''
Finds key statistics for a simple sankey graph showing cluster movement
between two consecutive snapshots
Input is a rtf file with the cluster movement percentages
'''
def track_sankey_flow(filename):
    ids = {}
    labels = []
    sources = []
    targets = []
    values = []
    current_key = -1
    volume = 0
    file_index = to_index(filename)
    inactive = "inactive" + "#" + parts[file_index + 1][:7]
    id = id_check(inactive, ids, 0, labels)
    for move in rtf_broker.movements(filename):
        clustera = move[0]
        clusterb = move[1]
        amount = move[2]
        # in
        in_key = clustera + '#' + parts[file_index][:7]

        # volume control
        if current_key == in_key:
            volume -= amount
        else:
            if volume > 0:
                # draw sink
                create_flow(current_key, inactive, volume, sources, targets, values, ids)
            current_key = in_key
            volume = 100 - amount

        # out
        out_key = clusterb + '#' + parts[file_index + 1][:7]
        id = id_check(in_key, ids, id, labels)
        id = id_check(out_key, ids, id, labels)
        create_flow(in_key, out_key, amount, sources, targets, values, ids)

    if volume > 0:
        # draw sink
        create_flow(current_key, inactive, volume, sources, targets, values, ids)
    name = parts[file_index][:7] + " to " + parts[file_index + 1][:7]
    vals = sankey.sanFlow(name, sources, targets, values, labels, filename)
    #for outgoing flow values
    flowVals(vals)

    #for percentage of inactive breakdown
    in_active(vals)

'''
Finds statistics for each flow. Finds mean, std dev, min, and max number of
flows leaving each source.
'''
def flowVals(vals):
    vals = vals['source']
    uniq = set(vals)
    array = []
    for each in uniq:
        array.append(vals.count(each))

    n_array = np.array(array)
    print("mean: ",n_array.mean())
    print("std: ",n_array.std())
    print("min: ",n_array.min())
    print("max: ",n_array.max())

'''
Finds percentage of the flows that go to the inactive destination
Finds min, max, mean, std dev. of number
'''
def in_active(vals):
    cluster = vals['target']
    vals = vals['value']
    dicts = dict()
    for i in range (0,len(cluster)):
        if cluster[i] in dicts:
            temp = dicts[cluster[i]]
            temp.append(vals[i])
            dicts[cluster[i]] = temp
        else:
            dicts[cluster[i]] = [vals[i]]

    index = 0
    maxLen = 0
    for each in dicts:
        tmp = len(dicts[each])
        if maxLen < tmp:
            maxLen = tmp
            index = each

    n_array = np.array(dicts[index])
    print("mean: ",n_array.mean())
    print("std: ",n_array.std())
    print("min: ",n_array.min())
    print("max: ",n_array.max())


'''
Takes a rtf file with the old cluster to new cluster stdout percentages and converts
to a bipartite graph, showing the older cluster moving to the new cluster
'''
def tracker(filename):
    G=nx.Graph()
    for move in rtf_broker.movements(filename):
        clustera = move[0]
        clusterb = move[1]
        amount = move[2]
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
uncomment main() to run functions in main(). Reconfigure as necessary
'''
if __name__ == '__main__':
    # main()
    #overall_sankey()
 #   filenames = [
 #       "Stats/" + file for file in rtf_broker.rtf_files()
 #   ]
 #   filename = filenames[10]
 #   track_sankey(filename)

    # track_sankey("Stats/B.rtf", passing=lambda amount: amount>8)
    #track_sankey("Stats/B.rtf")
    # track_sankey_flow("Stats/A.rtf")
    # track_sankey_flow("Stats/B.rtf")
    # track_sankey_flow("Stats/C.rtf")
    # track_sankey_flow("Stats/D.rtf")
    # track_sankey_flow("Stats/E.rtf")
    # track_sankey_flow("Stats/F.rtf")
    # track_sankey_flow("Stats/G.rtf")
    # track_sankey_flow("Stats/H.rtf")
    # track_sankey_flow("Stats/I.rtf")
    # track_sankey_flow("Stats/J.rtf")
    # track_sankey_flow("Stats/K.rtf")
    # track_sankey_flow("Stats/L.rtf")
    # track_sankey_flow("Stats/M.rtf")
 #   track_sankey_flow(filename)
    
    # track_sankey_high_pass(filename, 2)
    # track_sankey_low_pass(filename, 40)
