from os import listdir
from os.path import isfile, join
import sys
import nibabel as nib


def get_all_dcan_labels(labels_directory):
    labels = set()
    only_files = [f for f in listdir(labels_directory) if isfile(join(labels_directory, f))]
    for f in only_files:
        img = nib.load(join(labels_directory, f))
        data = img.get_fdata()
        shape = data.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    datum = int(data[i][j][k])
                    labels.add(datum)
        return list(labels)


if __name__ == "__main__":
    labels = get_all_dcan_labels(sys.argv[1])
    print(labels)
