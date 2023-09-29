#!/usr/bin/python
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join

from tqdm import tqdm


def rearrange_files(base_dir):
    for age in range(9):
        age_dir = os.path.join(base_dir, f'{age}mo')
        only_files = [f for f in listdir(age_dir) if isfile(join(age_dir, f))]
        for sub_dir_type in ['labels', 'T1w', 'T2w']:
            sub_dir = os.path.join(age_dir, sub_dir_type)
            sub_dir_exists = os.path.exists(sub_dir)
            if not sub_dir_exists:
                os.makedirs(sub_dir)
        for file in tqdm(only_files):
            if file.endswith('_0000.nii.gz'):
                shutil.move(join(age_dir, file), os.path.join(age_dir, 'T1w', file))
            elif file.endswith('_0001.nii.gz'):
                shutil.move(join(age_dir, file), os.path.join(age_dir, 'T2w', file))
            else:
                shutil.move(join(age_dir, file), os.path.join(age_dir, 'labels', file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='RearrangeLabelImageFiles',
        description='Rearrange files by age and file type')
    parser.add_argument('base_dir')
    args = parser.parse_args()
    rearrange_files(args.base_dir)
