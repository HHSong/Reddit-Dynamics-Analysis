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

def print_(res, flag):
    string = ""
    string2 = ""
    if flag:
        string = "goes to"
        string2 = "in the newer snapshot"
    else:
        string = "comes from"
        string2 = "in the older snapshot"
    for denom, numer in res:
        print("{0:.2f}% of cluster {1} {2} cluster {3} {4}".format(
            res[denom, numer] * 100, denom, string, numer, string2))

def print_old_to_new(res):
    print("Breakdown of dests of users in the older snapshot")
    print("-------------------------------------------------")
    print_(res, True)

def print_new_from_old(res):
    print("Breakdown of srcs of users in the newer snapshot")
    print("------------------------------------------------")
    print_(res, False)

''' 
Print functions added a typical use case looks as follows:
Assume we have the output of louvain algo of two consecutive snapshots
 output1 and output2

cluster_dict1, cluster_dict2 = create_newdict(output1, output2)
print_old_to_new(percentage_of(cluster_dict1, len(cluster_dict2), output2))
print_new_from_old(percentage_of(cluster_dict2, len(cluster_dict1), output1)))
'''