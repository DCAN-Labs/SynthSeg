import os.path
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

import nibabel as nib
import numpy as np


def estimate_intensities_by_age(task_dir, output_file):
    estimation_labels_file = './data/labels_classes_priors/dcan/labels.txt'
    file1 = open(estimation_labels_file, 'r')
    lines = file1.readlines()
    labels = []
    for line in lines:
        label = int(line.strip())
        labels.append(label)

    # need to give prior_means (the same applies to prior_stds) as a numpy array with K columns (the number of labels)
    # and 4 rows. The first two rows correspond to the [min, max] of the T1 contrast, and the 3rd and 4th rows
    # correspond to [min, max] of the T2 contrast.
    a = np.array([255, 0, 255, 0])
    mins_and_maxes_column_major = np.tile(a, [9, len(labels), 1])
    mins_and_maxes = np.transpose(mins_and_maxes_column_major, (0, 2, 1))

    labels_dir = os.path.join(task_dir, 'labelsTr')
    images_dir = os.path.join(task_dir, 'imagesTr')
    label_files = [f for f in listdir(labels_dir) if isfile(join(labels_dir, f))]
    for label_file_index in tqdm(range(len(label_files)), desc="file loop", position=1, leave=False):
        label_file = label_files[label_file_index]
        label_img = nib.load(join(labels_dir, label_file))
        label_data = label_img.get_fdata()
        t1_file = f'{label_file[:-7]}_0000.nii.gz'
        t1_file_path = os.path.join(images_dir, t1_file)
        t1_img = nib.load(t1_file_path)
        t1_data = t1_img.get_fdata()
        t2_file = f'{label_file[:-7]}_0001.nii.gz'
        t2_file_path = os.path.join(images_dir, t2_file)
        t2_img = nib.load(t2_file_path)
        t2_data = t2_img.get_fdata()
        data_shape = label_img.header.get_data_shape()
        for i in range(data_shape[0]):
            for j in range(data_shape[1]):                                                                                                    
                for k in range(data_shape[2]):
                    label = int(label_data[i][j][k])
                    label_index = labels.index(label)
                    age = int(label_file[0])
                    for contrast in range(2):
                        if contrast == 0:
                            voxel = int(t1_data[i][j][k])
                        else:
                            voxel = int(t2_data[i][j][k])
                        if voxel < 0:
                            voxel = 0
                        elif voxel > 255:
                            voxel = 255
                        row = contrast * 2
                        if voxel < mins_and_maxes[age][row][label_index]:
                            mins_and_maxes[age][row][label_index] = voxel
                        row = contrast * 2 + 1
                        if voxel > mins_and_maxes[age][row][label_index]:
                            mins_and_maxes[age][row][label_index] = voxel
    with open(output_file, 'wb') as f:
        # noinspection PyTypeChecker
        np.save(f, mins_and_maxes)


if __name__ == "__main__":
    task_folder = \
        '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg'
    output_fl = './data/labels_classes_priors/dcan/uniform/mins_maxes.npy'
    estimate_intensities_by_age(task_folder, output_fl)
