import pickle
import parser
import sys
import treeNode as tn
from time import sleep
from multiprocessing import Pool, Process, Manager
from os import walk, path, makedirs

sys.setrecursionlimit(50000)
dump_path = path.join('..', 'output')
reddit_path = path.join("..", 'redditHtmlData')
processed = []
output_data = {}


def list_files(dir_path):
    files = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        files.extend(filenames)
        break  # avoid recursion
    return list(
        filter(
            lambda file: not file[0] == '.',
            files
        )
    )


def list_raw_files():
    return list_files(reddit_path)


def list_dumped_files():
    return list_files(dump_path)


def pre_process():
    global processed
    processed = set(
        [dumped.rsplit('.', 1)[0] + '.html' for dumped in list_dumped_files()]
    )
    print("processed:" + str(processed))


def process(skip_processed=True):
    failed = []
    total = len(list_raw_files())
    count = 0
    percentage = 1
    for raw in list_raw_files():
        if skip_processed and raw in processed:
            continue
        # sleep(0.2)
        count += 1
        if count > percentage * total / 1000:
            print('proccessed {}%'.format(percentage/10))
            percentage += 1
        try:
            # print('processing: %s', raw)
            tree = parser.parse(
                path.join(reddit_path, raw)
            )
            if tree == 'deleted':
                continue
            for_each(tree)
            output = raw.rsplit('.', 1)[0] + '.dat'
            # save(tree, output)
            output_data[raw] = tree

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("error processing: " + raw)
            failed.append(raw)


def process_single(raw):
    return parser.parse(
        path.join(reddit_path, raw)
    )


def for_each(tree):
    # distants = tree.non_direct_descendants()
    # descendants = tree.descendants()
    pass


def post_process():
    save(output_data, "parsed_tree.dat")
    pass


def aggregate_edges(collection, edges):
    for edge in edges:
        key = frozenset([edge.master, edge.slave])
        if key not in collection:
            collection[key] = 0
        collection[key] += 1


def to_edges(tree):
    edges = []
    for desc in tree.non_direct_descendants():
        edges.append(
            init_distant_edge(tree, desc)
        )
    for child in tree.children:
        edges.append(
            init_close_edge(tree, child)
        )
    for child in tree.children:
        edges.extend(
            to_edges(child)
        )
    return edges


def init_distant_edge(master, slave):
    edge = tn.Edge()
    edge.master = master.user
    edge.slave = slave.user
    edge.weight = 1
    return edge


def init_close_edge(master, slave):
    edge = tn.Edge()
    edge.master = master.user
    edge.slave = slave.user
    edge.weight = 2
    return edge


def save(data, filename):
    if not path.exists(dump_path):
        makedirs(dump_path)
    filename = path.join(dump_path, filename)
    fileObject = open(filename, 'wb')
    pickle.dump(data, fileObject)
    fileObject.close()


def load(filename):
    filename = path.join(dump_path, filename)
    fileObject = open(filename, 'rb')
    return pickle.load(fileObject)


def parallel_process(raw):
    tree = parser.parse(
        path.join(reddit_path, raw)
    )
    output_data[raw] = tree


def multi_core():
    global output_data
    manager = Manager()
    output_data = manager.dict()
    pool = Pool(processes=4)
    pool.map(parallel_process, list_raw_files())

    save(output_data, path.join('output', "parallel.dat"))


if __name__ == "__main__":
    # pre_process()
    # process(skip_processed=False)
    # post_process()
    multi_core()
    pass
