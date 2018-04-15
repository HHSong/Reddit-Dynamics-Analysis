# Reddit Hammer: Tracking Reddit User Interests Over Time
-- by Wendy Li, Hao-Hsiang Song, Hao Mao, and Ben Y. Zhao\
Department of Computer Science, University of Chicago, Chicago, IL USA\
{wendyli, haohsiang, mouhao, ravenben}@uchicago.edu

### ABSTRACT
Data confidentiality policies of numerous popular social networks have severely limited researchers’ access to large-scale datasets. While there have been some studies pertaining to detailed dynamics of the movement of communities in large online social networks over time, there has been very little research done in terms of monitoring a content dataset and how users’ interest change over time. In this paper, we present the results of analyzing detailed dynamics of Reddit from July 2008 to Jan 2013. We analyze the dynamics at percommunity and network-wide granularities, determining how users’ interests shift over time. We find that, contrary to intuition, Reddit exhibits online social network properties, in which users interact together in different categories.

### Key Findings
Through our analysis, we found several significant findings. First, we find that overall, the network grows exponentially, which is expected for an OSN. Secondly, we also found that as the network gets bigger and takes off in popularity, user retain rate is higher and more and more interest communities stick together instead of disappearing or disassociating. In addition, we can identify clear evolutions in user interest over time, with certain topics being added and deleted through time and other topics rising in popularity over time. Finally, by analyzing user interest dynamics over time, we conclude that, unlike what intuition would suggest, Reddit acts not only as discussion forum, but also as an OSN.

### Processes

1. Data Parsing
We begin by defining an edge between two users as an interaction between two users. To find all such interactions, we build an HTML parser that parses out the usernames of a post’s author, the usernames of each commenter, the timestamps of each action, and the category of the post, denoted as the Subreddit tag. We processed 20GB of html archives with fully paralleled algorithm that leverages BeautifulSoup library for parsing. We were able to extract data with a 8-core CPU within 45 minutes.

2. Edge Creation
We defined direct interaction and indirect ones. Each of them formed an edge. We sucessfully extracted 6 millions of edges in our experiment. Particularly, we group the interaction data into the groups of the following snapshots according to its timestamp. For instance, the first and second snapshots would be from July 2008 to October 2008 and November 2008 to February 2009 respectively.

3. Community Construction
Communities are defined as network structure as clusters of well-connected nodes. These areas essentially have dense connections inside of the communities, but few or sparse connections outside of the communities. Thus, such a grouping would help to isolate various communities interest groups from each other in such a structure like the large OSN structure of Reddit. In particular, the Louvain algorithm is a scalable community detection algorithm that uses greedy local modularity optimization, making it significantly more scalable and efficient. 

4. Evolution Tracking
That is, we compute the percentage of a cluster that goes from one snapshot to another given cluster in the next snapshot, also identifying the percentage of new users emerging in a given clusters and the percentage of users in each cluster that disappears or drops out. To visualize our results, we utilize sankey diagrams depicting cluster movement from snapshot to snapshot. Each graph depicts the cluster movement between two consecutive snapshots. The lines or bars on the left side of the graph represent the communities in a snapshot of four months. The lines or bars on the right side of the graph represent the communities in the next snapshot of four months. The clusters are normalized and the width of the flow leaving each cluster or bar corresponds to the percentage of users leaving that cluster going to a cluster or bar in the second second snapshot. 

5. Interest Continuity
Interest continuity is defined as a user flow moving from one community to another community of the same interest or category and it is measured between two snapshots via flows. A flow is defined as users being grouped in a cluster in a previous snapshot forming a cluster, with or without others, in a later snapshot. When a group of users flows from a cluster to a future one, the dominating interests of the two source and destination clusters are compared, weighted by the relative size of the flow and then averaged. That is, the portion of users continuing on the same interest is calculated for each cluster. Finally, we plot the probability distribution of continuity rate across all clusters using the time span of four months.

6. Analyzing The Graphs
Through analyzing interest continuity across all the snapshots, it is evident that in the beginning of Reddit’s development, there is still a greater probability of 0% of the cluster showing interest continuity across all the earlier figures, meaning most users change interests. In these snapshots, for the rest of the interest continuities across clusters, there is also a more relatively even distribution, meaning some users in the clusters choose to maintain the same interest. However, especially starting from 2010-11, the time when Reddit begins its exponential growth in users, there becomes a much more polarized divide between user interest continuity as shown. As figures show, roughly half of the users choose to stay in the same category, while the other half of the users choose to switch categories. That is, almost 50% of clusters will have 100% of the cluster shift categories. The distribution turns bimodal.

7. Our Confirmation
If Reddit was purely a discussion forum and exhibited discussion forum behavior, then we would expect for the majority of users to remain in the same major interest category across snapshots. Nevertheless, clearly, half of the communities of Reddit will change categories, suggesting the OSN behavior of Reddit. Therefore, Reddit seems to act as a OSN for those who want to use it as such and interact together with other users in different categories.

### CONCLUSION
To conclude, we analyze the dynamics at percommunity and network-wide granularities, determining how users’ interests shift over time. We find that, contrary to intuition, Reddit exhibits properties of traditional OSNs, in which users interact together into different categories. Interestingly, as Reddit develops, there is a polarization in user interests shifts. Half of the users remain stagnant, concentrating on one topic of interest, while the other half of the users dramatically change interest categories from snapshot to snapshot, interacting with other users. Finally, user interest clearly change dynamically and shift throughout the snapshots.
