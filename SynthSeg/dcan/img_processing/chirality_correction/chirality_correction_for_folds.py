import glob
import os
import sys

from SynthSeg.dcan.img_processing.chirality_correction.chirality_correction_for_folder import correct_chirality
from SynthSeg.dcan.img_processing.chirality_correction.chirality_correction_of_manually_segmented_images import \
    get_paths


def correct_chirality_for_fold(input_folder, output_folder, fold):
    nnunet_folder = '/home/feczk001/shared/data/nnUNet/'
    paper_cross_validation_folder = 'segmentations/inferred/PaperCrossValidation/'
    nifti_input_folder_pth = os.path.join(input_folder, f'Fold{str(fold)}')
    data_dir = 'data'
    segment_lookup_tbl = \
        os.path.join('/home/miran045/reine097/projects/SynthSeg', data_dir,
                     'labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    nifti_input_file_pths = glob.glob(f"{nifti_input_folder_pth}/*.nii.gz")
    for nifti_input_file_pth in nifti_input_file_pths:
        filename, l_r_mask, output_mask_fl, sbjct_hd, tmplt_hd = get_paths(fold, nifti_input_file_pth, nnunet_folder,
                                                                           paper_cross_validation_folder)
        # the purpose here is to take the left right mask from the template and project it onto the native subject --
        # and then the chirality correction will use the subject-aligned left right mask to perform the correction
        # the aseg_mask is neither, its just a binary mask of the brain
        nifti_output_folder = os.path.join(output_folder, f'Fold{str(fold)}')
        correct_chirality(filename, l_r_mask, nifti_input_file_pth, nifti_output_folder, output_mask_fl, sbjct_hd,
                          segment_lookup_tbl, tmplt_hd)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    isExist = os.path.exists(output_dir)
    if not isExist:
        os.makedirs(output_dir)
    for fld in range(10):
        correct_chirality_for_fold(input_dir, output_dir, fld)
