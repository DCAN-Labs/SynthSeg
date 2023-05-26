import json
import os.path
import sys
from collections import OrderedDict
from os import listdir
from os.path import isfile, join

import nibabel as nib


def find_min_max(image_dir, labels_dir, age_in_months, contrast):
    only_files = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]
    contrast_code = '0000' if contrast.lower() == 't1w' else '0001'
    if age_in_months != 0:
        image_files_to_examine = \
            [f for f in only_files if f.startswith(f'{str(age_in_months)}mo') and f.endswith(f'{contrast_code}.nii.gz')]
    else:
        image_files_to_examine = \
            [f for f in only_files if 'ALBERT' in f and f.endswith(f'{contrast_code}.nii.gz')]
    label_to_min_max = OrderedDict()
    for f in image_files_to_examine:
        image_file_path = os.path.join(image_dir, f)
        base_f = f[:-len('_0000.nii.gz')]
        if age_in_months != 0:
            labels_file = f'{base_f}.nii.gz'
        else:
            labels_file = f'{base_f}_aseg.nii.gz'
        labels_file_path = os.path.join(labels_dir, labels_file)
        image_img = nib.load(image_file_path)
        # noinspection PyPep8
        try:
            labels_img = nib.load(labels_file_path)
        except:
            print(f'bad file: {labels_file_path}')

            continue
        image_image_data = image_img.get_fdata()
        image_image_data = image_image_data.squeeze()
        labels_image_data = labels_img.get_fdata()
        dims = image_image_data.shape
        for i in range(dims[0]):
            for j in range(dims[1]):
                for k in range(dims[2]):
                    label = int(labels_image_data[i][j][k])
                    pixel_val = image_image_data[i][j][k]
                    if label not in label_to_min_max.keys():
                        label_to_min_max[label] = [None, None]
                    if label_to_min_max[label][0] is None or pixel_val < label_to_min_max[label][0]:
                        label_to_min_max[label][0] = pixel_val
                    if label_to_min_max[label][1] is None or pixel_val > label_to_min_max[label][1]:
                        label_to_min_max[label][1] = pixel_val
    return label_to_min_max


def compute_min_max_by_age(base_dir):
    """
    Finds the min and max for each of the classes ranging over the files in the base directory.
    @param base_dir: the nnUNet_raw_data task directory
    """
    min_max_dict = OrderedDict()
    for age in range(9):
        if age not in min_max_dict.keys():
            min_max_dict[age] = OrderedDict()
        for file_type in ['T1w', 'T2w']:
            image_dir = os.path.join(base_dir, 'images')
            labels_dir = os.path.join(base_dir, 'labels')
            label_to_min_max = find_min_max(image_dir, labels_dir, age, file_type)
            min_max_dict[age][file_type] = label_to_min_max
    with open(os.path.join('./data/labels_classes_priors/dcan/uniform', "min_max_dict.json"), "w") as outfile:
        json.dump(min_max_dict, outfile, indent=4)


if __name__ == "__main__":
    compute_min_max_by_age(sys.argv[1])
