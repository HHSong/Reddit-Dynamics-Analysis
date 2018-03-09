%Do not change 
\documentclass[12pt, oneside]{article}
\usepackage{amssymb,amsmath}
\usepackage[margin=1in]{geometry}
\usepackage{textpos}
\usepackage{array}
\usepackage{geometry}
\usepackage{url}
\usepackage{stix}
\usepackage{fixltx2e}
\usepackage{textcomp}
\usepackage{textgreek}
\usepackage{mathtools}
\newcommand\floor[1]{\lfloor#1\rfloor}
\newcommand\ceil[1]{\lceil#1\rceil}
\usepackage{tikz}
\usetikzlibrary{arrows}
\usepackage{verbatim}
\usepackage{enumitem}
% You may add the packages you need here



\begin{document}
\begin{center}
\textbf{\Large Users' Interest Shift: A Reddit Data Analysis} \\
-- By Wendy Li, Hao-Hsiang Song, and Hao Mou
\end{center} 
\textbf{treeNode.py:} \\
$\indent \bullet           $   Contains the class for the TreeNode objects, which are used to parse the HTML files. \\
$\indent \bullet           $   Contains the class for the edges, which store the data for the interactions between users (data from parsing the HTML) \\
\\
\textbf{processor.py:}\\
$\indent \bullet           $   Main driver for parsing HTML files. \\
$\indent \bullet           $   Because of computational restrictions, we had to break the parsing into chunks and store the parsed data as partition files. \\
\\
\textbf{partitioner.py:}\\
$\indent \bullet           $   Functions for splitting the partitions into four month long snapshots.\\
\\
\textbf{parser.py}\\
$\indent \bullet           $   Contains functions that actually parse the HTML files to extract the relevant attributes and information. \\
\\
\textbf{constants.py:}\\
$\indent \bullet           $   Contains the names of the partitions (four month snapshots) of all parsed data.\\
\\
\textbf{compare.py:}\\
$\indent \bullet           $   Contains common\_user\_percentage, a function that finds the percentage of common users between the clusters in two snapshots.
\\
$\indent \bullet           $   Contains compare, a function that prints out the usernames of the common users in two snapshots.\\
\\
\textbf{movement\_btw\_snapshots.py}:\\
$\indent \bullet           $   Contains a helper function create\_newdict that preprocesses the dictionaries of the Louvain's algorithm.\\
$\indent \bullet           $   Contains percentage\_of, a function which calculates the fraction of a cluster in snapshot A that moves to a given cluster in snapshot B. Also calculates the percentage of a given cluster in snapshot B that comes from a given cluster in snapshot A. For example, 5 percent of cluster 1 in snapshot A goes to cluster 8 in snapshot B. \\
$\indent \bullet           $   Contains a print function that prints these statistics.\\
\\
\textbf{graph\_stats.py:}\\
$\indent \bullet           $   Contains functions that extract features like the average clustering coefficient, the degree assortativity, the degree assortativity for top categories, and the number of users for each snapshot. \\
$\indent \bullet           $   Contains functions that graph these statistics all on one graph.\\
\\
\textbf{try\_print.py:} \\
$\indent \bullet           $   Contains a toXGraph function that converts the snapshots (partition files) into an actual Networkx graph. toXGraph runs Louvain's algorithm and returns the clusters of the given snapshot.\\
$\indent \bullet           $   Contains a numCluster function that given the clusters of  given snapshot, counts the number of clusters in the graph\\
$\indent \bullet           $   Contains a getCategory function that given the clusters of a given snapshot, prints the unique categories in the snapshot and the number of occurrences of that category. Also prints out the total number of users.\\
$\indent \bullet           $   Contains a getAggregateCats function that finds the top categories for each snapshot.
\\
$\indent \bullet           $   Contains a getAvgCat function that finds statistics for number of different categories for each cluster in a snapshot. It finds the mean, standard deviation, minimum, and maximum.\\ \\
To run, "python3 try\_print.py -f [partition filename]". The partition filename is the snapshot we are running the program on, and we assume that file is located in a folder called "output".
\\
\\
\textbf{track.py:}
$\indent \bullet           $   Contains a tracker function that, taking a rtf file with the cluster movement between two snapshots percentages, converts these statistics into  bipartite graph, visualizing the old cluster moving to the new cluster. \\
$\indent \bullet           $   Contains track\_sankey, a function that takes a single rtf file input and produces a sankey graph. The rtf file input has the movement statistics from one snapshot to the next one. \\
$\indent \bullet           $   Contains a track\_sankey\_consolid function that works like the track\_sankey function, but specifies a particular threshold. Cluster movement below that threshold will not be visualized. \\
$\indent \bullet           $   Contains a overall\_sankey function that constructs the sankey graph for the first four snapshots, visualizing the movements of the clusters from snapshot to snapshot. \\
$\indent \bullet           $   Contains a track\_sankey\_flow function that finds the mean, maximum, minimum, and standard deviation of the number of flows leaving each source and the percentage of each source that goes inactive.\\
\\
To run, "python3 track.py". The command will output the overall sankey graph shown in the paper, which shows the cluster movement across the first four snapshots. There is also an option to run the other functions using commandline arguments (see the code for further documentation). \\
\\
\textbf{sankey.py:}\\
$\indent \bullet           $   Contains a helper function sankey, which track.py invokes to construct the sankey graphs. \\
$\indent \bullet           $   Contains a helper function sanFlow, which track.py invokes to get the information to determine the flow statistics that the track\_sankey\_flow function calculates.\\
\\
\textbf{print\_topcat.py:}\\
$\indent \bullet           $   Contains a print\_topcat function that prints the top categories and their respective percentages for each snapshot \\
$\indent \bullet           $   Contains plot\_percentage\_bar, a function that visualizes the percentage frequency distribution of  interactions in different subreddits across snapshots. \\
\\
To run, type "python3 print\_topcat.py".\\
\\
\textbf{rtf\_broker.py:}\\
$\indent \bullet           $   Contains functions that help manage the rtf files in constructing the sankey graphs. \\
\\
\textbf{get\_usernum.py:}\\
$\indent \bullet           $   Returns total number of users in our Reddit dataset.

Run by calling "python3 get\_usernum.py"\\
\\
\textbf{output Folder:}\\
$\indent \bullet           $   Contains all the raw partition data from the parsed HTML files.\\
$\indent \bullet           $   Partition files are our starting point after HTML parsing.
\\
\\
\textbf{Stats Folder:}\\
$\indent \bullet           $   Contains the intermediate data used for data analysis.\\
$\indent \bullet           $   For instance, A.rtf represents the raw data for the movement between the first and second snapshots.
\\
\\
\textbf{Distributions Folder:}\\
$\indent \bullet           $   Contains all the distribution graphs of user interest continuity.\\
\\
\textbf{Graphs with Inactive Folder:}\\
$\indent \bullet           $   Contains all the sankey graphs.\\
$\indent \bullet           $   Make sure to zoom all the way out to see the entire flow pattern.
\end{document}


