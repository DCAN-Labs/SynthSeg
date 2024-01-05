import argparse
import os.path
from os import listdir
from os.path import isfile, join


def create_split(base_folder, synth_seg_folder):
    for age in range(9):
        synth_seg_labels_folder = os.path.join(synth_seg_folder, 'labels')
        label_files = [f for f in listdir(synth_seg_labels_folder) if isfile(join(synth_seg_labels_folder, f))]
        stubs = [f[:-7] for f in label_files]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='split',
        description='Splits items into training and test sets')
    parser.add_argument('-b', '--base_dir')
    parser.add_argument('-s', '--synth_seg_dir')
    args = parser.parse_args()
    base_folder = args.base_dir
    synth_seg_folder = args.synth_seg_dir
    create_split(base_folder, synth_seg_folder)
