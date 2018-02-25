import treeNode
import pickle
from collections import Counter

files = ['2008-07', '2008-11', '2009-03', '2009-07', '2009-11', '2010-03', 
         '2010-07', '2011-03', '2011-07', '2011-11', '2012-03', '2012-07', 
         '2012-11']

def count_users(files):
    users = set([])
    for file in files:
        edges = []
        tmp_users = []
        with open('./output/' + file + '.partition', 'rb') as f:
            edges = pickle.load(f)
        for edge in edges:
            tmp_users.append(edge.getMaster())
            tmp_users.append(edge.getSlave())
        users = users | set(tmp_users)
    return len(users)


if __name__ == '__main__':
    print(count_users(files))