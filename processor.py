import pickle
import parser
import sys
import treeNode as tn
import shutil
from time import time
from multiprocessing import Pool, Manager
from os import walk, path, makedirs

sys.setrecursionlimit(50000)
dump_path = path.join('..', 'output')
reddit_path = path.join("..", 'redditHtmlData')
chunk_path = path.join("..", "chunk{}")
processed = []
output_data = {}
numberOfCheckPoints = 5
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
            for_each(tree)
            results[raw] = tree
        except (KeyboardInterrupt, SystemExit):
            print('error')
            raise
        except:
            print("error processing: " + raw)
            failed.append(raw)
    return results


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
    return parser.parse(
        raw
    )


def prepend_path(dir, file):
    return path.join(
        dir, file
    )


def update_processed_chunks(chunk_number):
    global processed
    output_files = list_files(
        chunk_path.format(chunk_number)
    )
    dumped_file = list(
        filter(
            lambda f: f == "chunk{}_processed.dat".format(chunk_number),
            output_files
        )
    )
    if len(dumped_file) == 0:
        return None
    processed = set(
        load(dumped_file[0])
    )
    print('processed chunks: %s', processed)


def split_files(files):
    split = []
    step = len(files) / numberOfCheckPoints
    next = step
    result = []
    for file in files:
        if len(split) > next:
            result.append(split)
            split = []
            next += step
        split.append(file)
    result.append(split)
    return result


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


def process_chunk_checkable(chunk_number):
    update_processed_chunks(chunk_number)
    chunk_dir = chunk_path.format(chunk_number)

    splits = split_files(
        list_files(chunk_dir)
    )

    for i in range(numberOfCheckPoints):
        process(
            [
                prepend_path(
                    chunk_dir, raw
                ) for raw in splits[i]
            ],
            skip_processed=True
        )
        print('finished: chunk{}_split{}', chunk_number, i)


def multi_core(starting_chunk, ending_chunk, processes=4):
    global output_data
    update_chunk_names()
    chunks = list(range(starting_chunk, ending_chunk+1, 1))
    with Pool(processes=processes) as pool:
        r = pool.imap_unordered(
                process_chunk,
                chunks
            )
        pool.close()
        pool.join()
        results = list(r)
        # output = dict(output_data)  # Manager().dict() is not pickle-able since it's a proxy
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


if __name__ == "__main__":
    start = time()
    # chunk_files(30)

    multi_core(0, 3, 4)

    print("execution time: {}s".format(
        time() - start
    ))

    # data = load(
    #     "processed_chunk0_3.dat"
    # )
    # print(data)