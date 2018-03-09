import pickle

import gc
from datetime import datetime

import parser
import sys
import treeNode as tn
import shutil
import partitioner
from time import time
from multiprocessing import Pool, Manager
from os import walk, path, makedirs

sys.setrecursionlimit(50000)
dump_path = path.join('..', 'output')
reddit_path = path.join("..", 'redditHtmlData')
chunk_path = path.join("..", "chunk{}")
processed = []
filenamesInEachChunks = {}


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


def process(raws, skip_processed=True):
    failed = []
    total = len(raws)
    count = 0
    percentage = 1
    results = {}
    for raw in raws:
        if skip_processed and raw in processed:
            continue
        count += 1
        if count > percentage * total / 100:
            print('proccessed {}%'.format(percentage))
            percentage += 1
        try:
            tree = parser.parse(
                raw
            )
            if tree == 'deleted':
                continue
            results[raw] = tree
        except (KeyboardInterrupt, SystemExit):
            print('Interrupted!')
            raise
        except:
            print("error processing: " + raw)
            failed.append(raw)
    return results


def process_single(raw):
    return parser.parse(
        raw
    )


def aggregate_edges(edges):
    results = []
    categories = aggregate_categories(edges)
    for pair, weight in aggregate_weights(edges).items():
        users = list(pair)
        node = tn.Edge()
        node.master = {
            'id': users[0],
            'categories': categories[users[0]]
        }
        node.slave = {
            'id': users[1],
            'categories': categories[users[1]]
        }
        node.weight = weight
        results.append(node)
    return results


def aggregate_categories(edges):
    collection = {}
    for edge in edges:
        key = edge.master
        if key not in collection:
            collection[key] = []
        collection[key].append(edge.category)
        key = edge.slave
        if key not in collection:
            collection[key] = []
        collection[key].append(edge.category)
    categories = {}
    for user, items in collection.items():
        categories[user] = list(set(items))
    return categories


def aggregate_weights(edges):
    collection = {}
    for edge in edges:
        if edge.master == edge.slave:
            continue
        key = frozenset([edge.master, edge.slave])
        collection[key] = collection.get(key, 0) + edge.weight
    return collection


def to_edges(tree):
    edges = []
    for desc in tree.non_direct_descendants():
        edges.append(
            init_edge(tree, desc, 1)
        )
    for child in tree.children:
        edges.append(
            init_edge(tree, child, 2)
        )
    for child in tree.children:
        edges.extend(
            to_edges(child)
        )
    return edges


def init_edge(master, slave, weight):
    edge = tn.Edge()
    edge.master = master.user
    edge.slave = slave.user
    edge.timestamp = string_to_datetime(
        slave.timestamp
    )
    edge.category = master.category
    edge.weight = weight
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


def prepend_path(dir, file):
    return path.join(
        dir, file
    )


def process_chunk(chunk_number):
    try:
        chunk_dir = chunk_path.format(chunk_number)
        results = process(
            [
                prepend_path(
                    chunk_dir, raw
                ) for raw in filenamesInEachChunks[chunk_number]
            ],
            skip_processed=True
        )
        print('finished: chunk{}', chunk_number)
        # print('results: {}', results)
        return results
    except:
        print('error')


def multi_core(starting_chunk, ending_chunk, processes=4):
    update_chunk_names()
    chunks = list(range(starting_chunk, ending_chunk+1, 1))
    with Pool(processes=processes) as pool:
        dictionary_of_trees = pool.imap_unordered(
                process_chunk,
                chunks
            )
        pool.close()
        pool.join()
        results = list(dictionary_of_trees)
    save(
        results,
        "processed_chunk{}_{}.dat".format(starting_chunk, ending_chunk)
    )
    print("saved chunk{}_{}".format(starting_chunk, ending_chunk))


def chunk_files(number):
    global filenamesInEachChunks
    files = list_raw_files()
    chunk = []
    count = 0
    for file in files:
        if len(chunk) > len(files) / number:
            move_files(chunk, chunk_path.format(count))
            filenamesInEachChunks[count] = chunk
            count += 1
            chunk = []
        chunk.append(file)
    filenamesInEachChunks[count] = chunk
    move_files(chunk, chunk_path.format(count))
    save(
        filenamesInEachChunks,
        "filenamesInEachChunks.dat"
    )


def update_chunk_names():
    global filenamesInEachChunks
    filenamesInEachChunks = load("filenamesInEachChunks.dat")


def move_files(files, folder):
    if not path.exists(folder):
        makedirs(folder)
    for file in files:
        shutil.move(
            path.join(
                reddit_path, file
            ),
            path.join(
                folder, file
            )
        )


def read_tree_data():
    files = filter(
        lambda file: file not in ["filenamesInEachChunks.dat", "data.edges"],
        list_dumped_files()
    )
    results = []
    for file in files:
        data = load(
            path.join(
                dump_path,
                file
            )
        )
        results.extend(data)
    return flatten_tree_data(results)


def edges_to_file(edges):
    save(
        edges,
        path.join(
            dump_path,
            "data.edges"
        )
    )


def string_to_datetime(string):
    return datetime.strptime(
        string,
        #'Sat Sep 22 01:26:16 2012 UTC'
        "%a %b %d %H:%M:%S %Y %Z"
    )


def convert_trees_to_edges(trees):
    edges = []
    for tree in trees:
        edges.extend(to_edges(tree))
    return edges


def flatten_tree_data(data):
    trees = []
    for d in data:
        if not (isinstance(d, dict)):
            print("none dictionary found: {}".format(d))
            continue
        for filename, tree in d.items():
            trees.append(tree)
    return trees


def load_edges():
    return load(
        path.join(
            dump_path,
            "data.edges"
        )
    )


def stat(edges):
    weights = {}
    for e in edges:
        weights[e.weight] = weights.get(e.weight, 1) + 1
    for k, v in weights.items():
        print('{} edges of weight {}'.format(v, k))


def multi_core_starter(start, end, processors):
    while (start <= end):
        print("starting {} to {}".format(start, start + processors - 1))
        multi_core(start, start + processors - 1)
        start += processors
        gc.collect()


def load_trees_convert_and_save(filename):
    trees = read_tree_data()
    edges = convert_trees_to_edges(trees)
    save(
        edges,
        path.join(
            dump_path,
            filename
        )
    )


def partition_and_save(edges):
    start_date = datetime(2012, 11, 1)
    end_date = datetime(2013, 2, 1)
    patitions = partitioner.partition_by_date(
        edges,
        start_date,
        end_date,
        4
    )
    months = partitioner.list_of_months(
        start_date,
        end_date,
        4
    )
    for i in range(len(months)-1):
        save(
            patitions[i],
            path.join(
                dump_path,
                months[i].strftime("%Y-%m") + ".partition"
            )
        )


def load_partition(date_string):
    return load(
        path.join(
            dump_path,
            date_string + ".partition"
        )
    )


def test_edges():
    edges = []
    e = tn.Edge()
    e.master = "a"
    e.slave = "b"
    e.category = "joke"
    edges.append(e)
    e = tn.Edge()
    e.master = "c"
    e.slave = "a"
    e.category = "pandas"
    edges.append(e)
    return edges


if __name__ == "__main__":
    start = time()

    edges = load_partition("2008-11")
    stat(edges)

    collected = aggregate_edges(edges)

    for collected_edge in collected:
        print(collected_edge)


    print("execution time: {}s".format(
        time() - start
    ))

