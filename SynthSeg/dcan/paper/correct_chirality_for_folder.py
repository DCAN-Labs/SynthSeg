import os.path
import re

import nibabel as nib

# Chirality-checking constants
from SynthSeg.dcan.look_up_tables import get_id_to_region_mapping

CHIRALITY_CONST = dict(UNKNOWN=0, LEFT=1, RIGHT=2, BILATERAL=3)
LEFT = "Left-"
RIGHT = "Right-"


def check_and_correct_region(should_be_left, region, segment_name_to_number,
                             new_data, chirality, floor_ceiling, scanner_bore):
    """
    Ensures that a voxel in NIFTI data is in the correct region by flipping
    the label if it's mislabeled

    Args:
        new_data: segmentation data passed by reference to be fixed if necessary
        segment_name_to_number: Map from anatomical regions to identifying numbers
        should_be_left: This voxel *should be on the LHS of the head
        region: String naming the anatomical region
        chirality: x-coordinate into new_data
        floor_ceiling: y-coordinate into new_data
        scanner_bore: z-coordinate into new_data
    """
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


def correct_chirality(nifti_input_file_path, segment_lookup_table,
                      left_right_mask_nifti_file, nifti_output_file_path):
    """
    Creates an output file with chirality corrections fixed.
    :param nifti_input_file_path: String, path to a segmentation file with possible chirality problems
    :param segment_lookup_table: String, path to a FreeSurfer-style look-up table
    :param left_right_mask_nifti_file: String, path to a mask file that distinguishes between left and right
    :param nifti_output_file_path: String, path to location to write the corrected file
    """
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
                if chirality_voxel == CHIRALITY_CONST["LEFT"] or chirality_voxel == CHIRALITY_CONST["RIGHT"]:
                    check_and_correct_region(
                        chirality_voxel == CHIRALITY_CONST["LEFT"], region, segment_name_to_number, new_data, i, j, k)
    fixed_img = nib.Nifti1Image(new_data, img.affine, img.header)
    nib.save(fixed_img, nifti_output_file_path)


if __name__ == "__main__":
    nn_unet_folder = '/home/feczk001/shared/data/nnUNet/'
    paper_cross_validation_folder = os.path.join(nn_unet_folder, 'segmentations/inferred/PaperCrossValidation/')
    lookup_table = '../../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
    l_r_mask_nifti_file = '/home/miran045/reine097/projects/CABINET/src/img_processing/Lmask.nii.gz'
    for subdir, dirs, files in os.walk(paper_cross_validation_folder):
        for file in files:
            file_path = os.path.join(subdir, file)
            print(file_path)
            if not file.endswith('.nii.gz'):
                continue
            p = re.compile('.*(Fold\d).*')
            m = p.match(file_path)
            fold_name = m.group(1)
            nifti_input_file = file_path
            nifti_output_folder = os.path.join(paper_cross_validation_folder, f'chirality_corrected/{fold_name}')
            is_exist = os.path.exists(nifti_output_folder)
            if not is_exist:
                os.makedirs(nifti_output_folder)
            nifti_output_file = os.path.join(nifti_output_folder, f'{file}')
            t1w_path = os.path.join(nn_unet_folder, f'raw_data/Task516_525/gt_labels/{fold_name}/{file}')

            correct_chirality(nifti_input_file, lookup_table,
                              l_r_mask_nifti_file, nifti_output_file)
