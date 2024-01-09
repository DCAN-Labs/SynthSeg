import os
import sys
from os import listdir
from os.path import isfile, join
import nibabel as nib
import operator


def main(base_dir) -> int:
    size_to_count = dict()
    only_files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
    for f in only_files:
        img = nib.load(join(base_dir, f))
        header = img.header
        data_shape = header.get_data_shape()
        if data_shape not in size_to_count:
            size_to_count[data_shape] = []
        size_to_count[data_shape].append(f)
    sorted_d = dict(sorted(size_to_count.items(), key=operator.itemgetter(1), reverse=True))
    keys = sorted_d.keys()
    for key in keys:
        sub_folder = f'{key[0]}_{key[1]}_{key[2]}'
        path = os.path.join(base_dir, sub_folder)
        exists = os.path.exists(path)
        if not exists:
            os.makedirs(path)
        values = sorted_d[key]
        for value in values:
            os.rename(os.path.join(base_dir, value), os.path.join(path, value))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
