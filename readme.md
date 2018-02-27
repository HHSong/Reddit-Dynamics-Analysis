Users' Interest Shift: A Reddit Data Analysis
-- By Wendy Li, Hao-Hsiang Song, and Hao Mou




try_print.py:
~Contains a toXGraph function that converts the snapshots (partition files) into an actual Networkx graph. toXGraph runs Louvain's algorithm and returns the clusters of the given snapshot.
~Contains a numCluster function that given the clusters of  given snapshot, counts the number of clusters in the graph
~Contains a getCategory function that given the clusters of a given snapshot, prints the unique categories in the snapshot and the number of occurrences of that category. Also prints out the total number of users.
~Contains a getAggregateCats function that finds the top categories for each snapshot.

To run, "python3 try_print.py -f [partition filename]". The partition filename is the snapshot we are running the program on, and we assume that file is located in a folder called "output".


track.py:
~Contains a tracker function that, taking a rtf file with the cluster movement between two snapshots percentages, converts these statistics into  bipartite graph, visualizing the old cluster moving to the new cluster.
~Contains track_sankey, a function that takes a single rtf file input and produces a sankey graph. The rtf file input has the movement statistics from one snapshot to the next one.
~Contains a track_sankey_consolid function that works like the track_sankey function, but specifies a particular threshold. Cluster movement below that threshold will not be visualized.
~Contains a overall_sankey function that constructs the sankey graph for the first four snapshots, visualizing the movements of the clusters from snapshot to snapshot.

To run, "python3 track.py". The command will output the overall sankey graph shown in the paper, which shows the cluster movement across the first four snapshots. There is also an option to run the other functions using commandline arguments (see the code for further documentation).


sankey.py:
~Contains a helper function sankey, which track.py invokes to construct the sankey graphs.


print_topcat.py:
~Contains a print_topcat function that prints the top categories and their respective percentages for each snapshot
~Contains plot_percentage_bar, a function that visualizes the percentage frequency distribution of  interactions in different subreddits across snapshots.

To run, type "python3 print_topcat.py".

