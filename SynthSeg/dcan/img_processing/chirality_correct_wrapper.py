#!/usr/bin/env python

"""
This script uses the LR mask to correct the chirality of segmentations generated with nnUNet. The final aseg will be
output to:
/home/exacloud/gscratch/InspireLab/data/HCP/processed/ECHO/pipeline_inputs/nnunet/asegs_cc

Arguments:

Usage:
  chirality_correct_wrapper  <job_name>
  chirality_correct_wrapper -h | --help
Options:
  -h --help     Show this screen.

"""
import nibabel as nib
import os
import glob

CHIRALITY_CONST = dict(UNKNOWN=0, LEFT=1, RIGHT=2, BILATERAL=3)
LEFT = 'Left-'
RIGHT = 'Right-'


def get_id_to_region_mapping(mapping_file_name, separator=None):
    file = open(mapping_file_name, 'r')
    lines = file.readlines()

    id_to_region = {}
    for line in lines:
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        if separator:
            parts = line.split(separator)
        else:
            parts = line.split()
        region_id = int(parts[0])
        region = parts[1]
        id_to_region[region_id] = region
    return id_to_region


def check_and_correct_region(should_be_left, region, segment_name_to_number, new_data, chirality,
                             floor_ceiling, scanner_bore):
    if should_be_left:
        expected_prefix = LEFT
        wrong_prefix = RIGHT
    else:
        expected_prefix = RIGHT
        wrong_prefix = LEFT
    if region.startswith(wrong_prefix):
        flipped_region = expected_prefix + region[len(wrong_prefix):]
        flipped_id = segment_name_to_number[flipped_region]
        new_data[chirality][floor_ceiling][scanner_bore] = flipped_id


def correct_chirality(nifti_input_file_path, segment_lookup_table, left_right_mask_nifti_file, nifti_output_file_path):
    free_surfer_label_to_region = get_id_to_region_mapping(segment_lookup_table)
    segment_name_to_number = {v: k for k, v in free_surfer_label_to_region.items()}
    img = nib.load(nifti_input_file_path)
    data = img.get_data()
    left_right_img = nib.load(left_right_mask_nifti_file)
    left_right_data = left_right_img.get_data()

    new_data = data.copy()
    data_shape = img.header.get_data_shape()
    left_right_data_shape = left_right_img.header.get_data_shape()
    width = data_shape[0]
    height = data_shape[1]
    depth = data_shape[2]
    assert \
        width == left_right_data_shape[0] and height == left_right_data_shape[1] and depth == left_right_data_shape[2]
    for i in range(width):
        for j in range(height):
            for k in range(depth):
                voxel = data[i][j][k]
                region = free_surfer_label_to_region[voxel]
                chirality_voxel = int(left_right_data[i][j][k])
                if not (region.startswith(LEFT) or region.startswith(RIGHT)):
                    continue
                if chirality_voxel == 1 or chirality_voxel == 2:
                    check_and_correct_region(
                        chirality_voxel == 1, region, segment_name_to_number, new_data, i, j, k)
    fixed_img = nib.Nifti1Image(new_data, img.affine, img.header)
    nib.save(fixed_img, nifti_output_file_path)


def wrapper():
    asegs_pre_cc_dir = '/home/faird/shared/code/internal/pipelines/CABINET/data/template_input_asegs/'
    lr_mask_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/LR_masks/'
    asegs_cc_dir = '/home/faird/shared/code/internal/pipelines/CABINET/data/template_input_asegs/'
    data_dir = '/home/miran045/reine097/projects/SynthSeg/data/'
    segment_lut = os.path.join(data_dir, 'labels_classes_priors/dcan/FreeSurferColorLUT.txt')

    os.chdir('{}'.format(asegs_pre_cc_dir))
    sublist = glob.glob('*nii.gz')
    sublist.sort()

    for aseg in sublist:
        aseg_strip = aseg.strip('.nii.gz')
        split_name = aseg_strip.split("_", 2)
        sub = split_name[0]
        subses = split_name[0] + '_' + split_name[1]

        if not os.path.exists('{}/{}_aseg.nii.gz'.format(asegs_cc_dir, subses)):
            print('Correcting chirality for {} segmentation: \n'
                  '{}/{}'.format(subses, asegs_pre_cc_dir, aseg))

            if os.path.exists('{}/{}/LRmask.nii.gz'.format(lr_mask_dir, subses)):
                print('Using {}/{}/LRmask.nii.gz for chirality correction'.format(lr_mask_dir, subses))

                lr_mask = '{}/{}/LRmask.nii.gz'.format(lr_mask_dir, subses)
                outfile = '{}/{}_aseg.nii.gz'.format(asegs_cc_dir, subses)

                inputaseg = '{}/{}'.format(asegs_pre_cc_dir, aseg)

                correct_chirality(inputaseg, segment_lut, lr_mask, outfile)

            else:
                print('No LR mask for {} - exiting'.format(sub))

        else:
            print('Corrected aseg file {}/{}_aseg.nii.gz already exists'.format(asegs_cc_dir, subses))


if __name__ == '__main__':
    wrapper()
