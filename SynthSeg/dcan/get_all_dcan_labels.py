import sys


def get_all_dcan_labels(labels_file_path):
    with open(labels_file_path) as fp:
        lines = fp.readlines()
        lbls = [int(line.strip()) for line in lines]
    return lbls


if __name__ == "__main__":
    labels = get_all_dcan_labels(sys.argv[1])
    print(labels)
