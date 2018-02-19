def create_newdict(output1, output2):
    # create_newdict takes the output dictionaries of louvain algo and
    #  outputs two dictionaries with key - item = cluster - user
    dict1 = {}
    dict2 = {}
    for i in range(len(output1)):
        dict1[i] = []
    for i in range(len(output2)):
        dict2[i] = []
    for key in output1:
        dict1[output1[key]].append(key)
    for key in output2:
        dict2[output2[key]].append(key)
    return dict1, dict2

def percentage_of(cluster_dict, numNewCluster, user_dict):
    # percentage_of calculates how users move from snapshot A
    #  to snapshot B as a fraction of clusters in snapshot A
    # percentage_of takes the cluster_dict of snapshot A (output 
    #  of create_newdict) and the user_dict of snapshot B (output
    #  of the louvain algo)
    # numNewCluster = len(cluster_dict of snapshot B)
    res = {}
    for cluster in cluster_dict:
        numUsers = len(cluster_dict[cluster])
        for i in range(numCluster):
            res[cluster, i] = 0
        for user in cluster_dict[cluster]:
            tmp[cluster, user_dict[user]] += 1
        for i in range(numCluster):
            tmp[cluster, i] /= numUsers
    return res