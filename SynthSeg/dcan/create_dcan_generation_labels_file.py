import numpy as np
import sys


def create_dcan_generation_labels_file(filename, out_file, add_zero=False):
    labels = []
    if add_zero:
        labels.append(0)
    with open(filename) as f:
        for index, line in enumerate(f):
            line = line.strip()
            if len(line) > 0:
                print("Line {}: {}".format(index, line))
                if line[0] != '#':
                    parts = line.split()
                    label = int(parts[0])
                    labels.append(label)
    np_array = np.array(labels)
    np.save(out_file, np_array)


if __name__ == "__main__":
    create_dcan_generation_labels_file(sys.argv[1], sys.argv[2])
