"""
Correct chirality.
Usage:
  correct_chirality <nifti_input_file_path> <segment_lookup_table> <left_right_mask_nifti_file> <nifti_output_file_path>
  correct_chirality -h | --help
Options:
  -h --help     Show this screen.
"""
import os

import nibabel as nib

from SynthSeg.dcan.img_processing import chirality_constants
from SynthSeg.dcan.look_up_tables import get_id_to_region_mapping

RIGHT = 'Right-'
LEFT = 'Left-'


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
                chirality_voxel = int(left_right_data[i][j][k])
                if chirality_voxel == chirality_constants.UNKNOWN or chirality_voxel == chirality_constants.BILATERAL:
                    continue
                region = free_surfer_label_to_region[voxel]
                if chirality_voxel == chirality_constants.LEFT:
                    check_and_correct_region(True, region, segment_name_to_number, new_data, i, j, k)
                elif chirality_voxel == chirality_constants.RIGHT:
                    check_and_correct_region(False, region, segment_name_to_number, new_data, i, j, k)
    fixed_img = nib.Nifti1Image(new_data, img.affine, img.header)
    nib.save(fixed_img, nifti_output_file_path)


if __name__ == "__main__":
    nnunet_folder = '/home/feczk001/shared/data/nnUNet/'
    nifti_input_file_pth = os.path.join(
            nnunet_folder,
            'segmentations/inferred/PaperCrossValidation/original/Task516_Paper_Fold0/0mo_template_07.nii.gz')
    data_dir = '/home/miran045/reine097/projects/SynthSeg/data/'
    segment_lookup_tbl = os.path.join(data_dir, 'labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    left_right_mask_nifti_fl = \
        '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/orig_chircorr_templates/' \
        '1mo_template_LRmask.nii.gz'
    paper_cross_validation_folder = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/'
    nifti_output_file_pth = \
        os.path.join(paper_cross_validation_folder, 'chirality_corrected/0mo_template_07.nii.gz')
    correct_chirality(nifti_input_file_pth, segment_lookup_tbl, left_right_mask_nifti_fl, nifti_output_file_pth)
