def dump_all_clusters():
    files = processor.list_files("output")
    partitions = list(
        filter(
            lambda f: "partition" in f,
            files
        )
    )
    results = {}
    for i in range(len(partitions)):
        filename = partitions[i]
        p = toXGraph(filename)[0]
        results[filename] = p
        print("processed: " + filename)

    with open("output/all_clusters.json", 'w') as f:
        json.dump(results, f)


def map_clusters():
    with open("output/all_clusters.json", 'r') as f:
        datastore = json.load(f)
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

    results = []
    for i in range(len(parts)-1):
        mapping = {}
        nameA = parts[i]
        nameB = parts[i+1]
        A = datastore[nameA]
        B = datastore[nameB]
        for user, clusterA in A.items():
            if user not in B:
                continue
            clusterB = B[user]
            if clusterA in mapping:
                if mapping[clusterA] != clusterB:
                    print("error: " + user)
                continue
            mapping[clusterA] = clusterB
        results.append(mapping)

    with open("output/cluster_mapping.json", 'w') as f:
        json.dump(results, f)






def getTotal(partition):
    '''
Helper function to getAggregate Cats that finds the index of the number of
total clusters in the snapshot
    '''
    count = 0
    for each in partition:
        count += 1
    return count



def pie(ax, center):
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)
    ax.pie(sizes,
           # autopct='%1.1f%%',
           # shadow=True,
           startangle=90, radius=0.15, center=center)
