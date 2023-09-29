import argparse
import os
import os.path
import random
from os import listdir
from os.path import isfile, join
import shutil


def move_files(stems, src_labels_dir, dest_labels_folder, src_t1_dir, src_t2_dir, dest_images_folder):
    for stem in stems:
        label_file = f'{stem}.nii.gz'
        label_file_path = os.path.join(src_labels_dir, label_file)
        shutil.move(label_file_path, dest_labels_folder)
        t1_file = f'{stem}_0000.nii.gz'
        t1_file_path = os.path.join(src_t1_dir, t1_file)
        shutil.move(t1_file_path, dest_images_folder)
        t2_file = f'{stem}_0001.nii.gz'
        t2_file_path = os.path.join(src_t2_dir, t2_file)
        shutil.move(t2_file_path, dest_images_folder)


def create_split(base_dir):
    labels_ts = os.path.join(base_dir, 'labelsTs')
    is_exist = os.path.exists(labels_ts)
    if not is_exist:
        os.makedirs(labels_ts)
    images_tr = os.path.join(base_dir, 'imagesTr')
    is_exist = os.path.exists(images_tr)
    if not is_exist:
        os.makedirs(images_tr)
    images_ts = os.path.join(base_dir, 'imagesTs')
    is_exist = os.path.exists(images_ts)
    if not is_exist:
        os.makedirs(images_ts)
    labels_tr = os.path.join(base_dir, 'labelsTr')
    is_exist = os.path.exists(labels_tr)
    if not is_exist:
        os.makedirs(labels_tr)

    for age in range(9):
        month_folder = os.path.join(base_dir, f'{str(age)}mo')
        labels_dir = os.path.join(month_folder, 'labels')
        age_label_files = [f for f in listdir(labels_dir) if isfile(join(labels_dir, f))]
        file_count = len(age_label_files)
        test_size = int(round(0.2 * file_count))
        stems = list(map(lambda label_file_name: label_file_name[:-7], age_label_files))
        test_stems = random.sample(stems, test_size)
        train_stems = [stem for stem in stems if stem not in test_stems]
        t1_dir = os.path.join(month_folder, 'T1w')
        t2_dir = os.path.join(month_folder, 'T2w')
        move_files(test_stems, labels_dir, labels_ts, t1_dir, t2_dir, images_ts)
        move_files(train_stems, labels_dir, labels_tr, t1_dir, t2_dir, images_tr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='split',
        description='Splits items into training and test sets')
    parser.add_argument('-b', '--base_dir')
    args = parser.parse_args()
    base_folder = args.base_dir
    create_split(base_folder)
