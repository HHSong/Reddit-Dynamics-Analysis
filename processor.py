import pickle
import parser
import sys
import treeNode as tn
import shutil
from time import sleep, time
from multiprocessing import Pool, Process, Manager
from os import walk, path, makedirs

sys.setrecursionlimit(50000)
dump_path = path.join('..', 'output')
reddit_path = path.join("..", 'redditHtmlData')
chunk_path = path.join("..", "chunk{}")
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


def process(raws, skip_processed=True):
    failed = []
    total = len(raws)
    count = 0
    percentage = 1
    for raw in raws():
        if skip_processed and raw in processed:
            continue
        count += 1
        if count > percentage * total / 1000:
            print('proccessed {}%'.format(percentage/10))
            percentage += 1
        try:
            tree = parser.parse(
                path.join(reddit_path, raw)
            )
            if tree == 'deleted':
                continue
            for_each(tree)
            # output = raw.rsplit('.', 1)[0] + '.dat'
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
    return parser.parse(
        raw
    )


def prepend_path(dir, file):
    return path.join(
        dir, file
    )


def process_chunk(chunk_number):
    raw_files = list_files(
        chunk_path.format(chunk_number)
    )
    process(raw_files, False)
    save(
        output_data,
        path.join(
            dump_path,
            "chunk{}.out.dat".format(chunk_number)
        )
    )


def multi_core(processes=4):
    pool = Pool(processes=processes)
    chunk_files(processes)
    results = pool.imap_unordered(
        process_chunk,
        range(processes)
    )
    pool.close()
    pool.join()



    # dir = chunk_path.format(chunk_number)
    # files = list_files(dir)
    # files = [prepend_path(dir, file) for file in files]
    # results = pool.imap_unordered(
    #     parallel_process,
    #     files
    # )
    # output = []
    # pool.close()
    # pool.join()
    # for result in results:
    #     if result is None: continue
    #     output.append(result)
    # save(output, path.join(dump_path, "chunk{}.dat".format(chunk_number)))


def chunk_files(number):
    files = list_raw_files()
    chunk = []
    count = 0
    for file in files:
        if len(chunk) > len(files) / number:
            move_files(chunk, chunk_path.format(count))
            count += 1
            chunk = []
        chunk.append(file)
    move_files(chunk, chunk_path.format(count))


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
    # pre_process()
    # process(skip_processed=False)
    # post_process()
    multi_core(4)
    # chunk_files()

    print("execution time: {}s".format(
        time() - start
    ))
    pass

