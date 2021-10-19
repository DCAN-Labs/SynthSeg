import numpy as np
import sys

from SynthSeg.dcan.segmentation_common import get_generation_labels


def create_dcan_generation_labels_file(out_file):
    labels = get_generation_labels()
    np_array = np.array(labels)
    np.save(out_file, np_array)


if __name__ == "__main__":
    create_dcan_generation_labels_file(sys.argv[1])
