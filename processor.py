import pickle
import parser
import sys
from os import walk, path, makedirs

sys.setrecursionlimit(50000)
dump_path = path.join('..', 'output')
reddit_path = path.join("..", 'redditHtmlData')
processed = []

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


def process(skip_processed = True):
    failed = []
    for raw in list_raw_files():
        if skip_processed and raw in processed:
            continue
        try:
            tree = parser.parse(
                path.join(reddit_path, raw)
            )
            if tree == 'deleted':
                continue
            for_each(tree)
            output = raw.rsplit('.', 1)[0] + '.dat'
            save(tree, output)
        except:
            print("error processing: " + raw)
            failed.append(raw)


def process_single(raw):
    tree = parser.parse(
        path.join(reddit_path, raw)
    )


def for_each(tree):
    # distants = tree.non_direct_descendants()
    # descendants = tree.descendants()
    pass


def post_process():
    pass


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


if __name__ == "__main__":
    pre_process()
    process()
    post_process()
    pass