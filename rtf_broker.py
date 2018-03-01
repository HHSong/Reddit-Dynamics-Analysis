import string


def rtf_files():
    rtfs = []
    for letter in string.ascii_uppercase[:13]:
        rtfs.append(letter + ".rtf")
    return rtfs


def to_index(filename):
    filename = filename[filename.index(".")-1:]
    return ord(filename[0:1]) - 65


def strip_lines(f):
    out = []
    to_skip = True
    for line in f:
        if to_skip and "CocoaLigature0" not in line:
            continue
        if "CocoaLigature0" in line:
            to_skip = False
            i = line.index("CocoaLigature0")
            out.append(line[i + len("CocoaLigature0") + 2:])
            continue
        out.append(line)
    return out


def movements(filename):
    '''get a list of tuples with (clusterA, clusterB, percentage_move)'''
    moves = []
    with open(filename, 'r') as f:
        f = strip_lines(f)
        for line in f:
            newline = line.split('%')
            amount = float(newline[0])
            newline = newline[1].split()
            clustera = newline[2]
            clusterb = newline[6]
            moves.append(
                (clustera, clusterb, amount)
            )
    return moves
