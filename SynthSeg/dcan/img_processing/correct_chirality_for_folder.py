# Author: Paul Reiners

import os
from os.path import exists

from SynthSeg.dcan.img_processing.left_right_registration_correction import left_right_registration_correction


def process_file(fold_number, file_base_name):
    nnunet_folder = '/home/feczk001/shared/data/nnUNet/'
    sbjct_hd = \
        os.path.join(
            nnunet_folder, 'nnUNet_raw_data_base', 'nnUNet_raw_data',
            f'Task{516 + fold_number}_Paper_Fold{fold_number}', 'imagesTs', f'{file_base_name}_0000.nii.gz')
    data_dir = '/home/miran045/reine097/projects/SynthSeg/data/'
    tmplt_hd = os.path.join(data_dir, 'sub-00006_T1w_acpc_dc_restore.nii.gz')
    nifti_input_file_pth = \
        os.path.join(
            nnunet_folder, 'segmentations', 'inferred', 'PaperCrossValidation',
            f'Task{516 + fold_number}_Paper_Fold{fold_number}', f'{file_base_name}.nii.gz')
    segment_lookup_tbl = os.path.join(data_dir, 'labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    l_r_mask = os.path.join(data_dir, 'sub-00006_ses-20170806_aseg_mask.nii.gz')
    paper_cross_validation_folder = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/'
    output_mask_fl = \
        os.path.join(paper_cross_validation_folder, f'chirality_correction_masks/{file_base_name}_LRmask.nii.gz')
    output_folder = \
        os.path.join(
            paper_cross_validation_folder, f'chirality_corrected/Task{516 + fold_number}_Paper_Fold{fold_number}/')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    nifti_output_file_pth = os.path.join(output_folder, f'{file_base_name}.nii.gz')
    if not exists(nifti_output_file_pth):
        left_right_registration_correction(
            sbjct_hd, tmplt_hd, nifti_input_file_pth, segment_lookup_tbl, l_r_mask, output_mask_fl,
            nifti_output_file_pth)


def correct_chirality_for_folder():
    cross_validation_folder = \
        '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/'
    for i in range(10):
        subfolder_name = f'Task{516 + i}_Paper_Fold{i}'
        input_folder = os.path.join(cross_validation_folder, subfolder_name)
        for filename in os.listdir(input_folder):
            if filename.endswith(".nii.gz"):
                print("Processing:", filename)
                process_file(i, filename[:-7])
            else:
                continue


if __name__ == '__main__':
    correct_chirality_for_folder()
