# Author: Paul Reiners

import sys


def get_all_dcan_labels(labels_file_path):
    with open(labels_file_path) as fp:
        lines = fp.readlines()
        index = 0
        while not lines[index].startswith('labels'):
            index += 1
        index += 1
        lbls = [int(line[:2].strip()) for line in lines[index:]]
    return lbls


if __name__ == "__main__":
    labels = get_all_dcan_labels(sys.argv[1])
    print(labels)
