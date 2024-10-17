import argparse
import os.path
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

import nibabel as nib
import numpy as np


def estimate_intensities_by_age(task_dir, output_file, tqdm_position=1, tqdm_leave=False):
    """
    Computes SynthSeg uniform priors for ages 0 through 9 (months).
    @param tqdm_leave:   : bool, optional
            For tqdm, if [default: True], keeps all traces of the progressbar
            upon termination of iteration.
    @param tqdm_position:   : int, optional
            For tqdm, pecify the line offset to print this bar (starting from 0)
            Automatic if unspecified.
            Useful to manage multiple bars at once (eg, from threads).
    @param task_dir: The nnU-Net task folder from which to read the priors.
    @param output_file: Priors for ages 0 through 9 are all stored in this file.
    @return: None
    """
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

    for label_file_index in tqdm(range(len(label_files)), desc="file loop", position=tqdm_position, leave=tqdm_leave):
        label_file = label_files[label_file_index]
        label_img = nib.load(join(labels_dir, label_file))
        label_data = label_img.get_fdata()

        t1_file = f'{label_file[:-7]}_0000.nii.gz'
        t1_file_path = os.path.join(images_dir, t1_file)
        t2_file = f'{label_file[:-7]}_0001.nii.gz'
        t2_file_path = os.path.join(images_dir, t2_file)

        t1_data = None
        t2_data = None

        if os.path.isfile(t1_file_path):
            t1_img = nib.load(t1_file_path)
            t1_data = t1_img.get_fdata()

        if os.path.isfile(t2_file_path):
            t2_img = nib.load(t2_file_path)
            t2_data = t2_img.get_fdata()

        if t1_data is None and t2_data is None:
            print(f"Neither T1 or T2 image found for {label_file}")
        else:
            process_image(label_img, label_data, t1_data, t2_data, labels, mins_and_maxes, label_file)
    
    with open(output_file, 'wb') as f:
        # noinspection PyTypeChecker
        np.save(f, mins_and_maxes)
    
def process_image(label_img, label_data, t1_data, t2_data, labels, mins_and_maxes, label_file):
        data_shape = label_img.header.get_data_shape()
        for i in range(data_shape[0]):
            for j in range(data_shape[1]):                                                                                                    
                for k in range(data_shape[2]):
                    label = int(label_data[i][j][k])
                    label_index = labels.index(label)
                    age = int(label_file[0])

                    if t1_data is not None and t2_data is not None:
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
                    elif t1_data is not None:
                        voxel = int(t1_data[i][j][k])
                        if voxel < 0:
                            voxel = 0
                        elif voxel > 255:
                            voxel = 255
                        row = 2
                        if voxel < mins_and_maxes[age][row][label_index]:
                            mins_and_maxes[age][row][label_index] = voxel
                        row += 1
                        if voxel > mins_and_maxes[age][row][label_index]:
                            mins_and_maxes[age][row][label_index] = voxel
                    else:
                        voxel = int(t2_data[i][j][k])
                        if voxel < 0:
                            voxel = 0
                        elif voxel > 255:
                            voxel = 255
                        row = 2
                        if voxel < mins_and_maxes[age][row][label_index]:
                            mins_and_maxes[age][row][label_index] = voxel
                        row += 1
                        if voxel > mins_and_maxes[age][row][label_index]:
                            mins_and_maxes[age][row][label_index] = voxel



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='uniform_intensity_by_age',
        description='Computes SynthSeg uniform priors for ages 0 through 9.',
        epilog='Please contact reine097 for questions or problems.')
    parser.add_argument('task_folder')
    parser.add_argument('output_fl')
    args = parser.parse_args()
    estimate_intensities_by_age(args.task_folder, args.output_fl, tqdm_position=0, tqdm_leave=True)
