import glob
import os
from os.path import exists
import sys

from SynthSeg.dcan.img_processing.chirality_correction.left_right_registration_correction import \
    left_right_registration_correction


def correct_chirality(filename, l_r_mask, nifti_input_file_pth, nifti_output_folder, output_mask_fl, sbjct_hd,
                      segment_lookup_tbl, tmplt_hd):
    is_exist = os.path.exists(nifti_output_folder)
    if not is_exist:
        os.makedirs(nifti_output_folder)
    nifti_output_file_pth = os.path.join(nifti_output_folder, filename)
    file_exists = exists(nifti_output_file_pth)
    if not file_exists:
        method_call = f"""left_right_registration_correction(
                '{sbjct_hd}', '{tmplt_hd}', '{nifti_input_file_pth}', '{segment_lookup_tbl}', '{l_r_mask}', 
                '{output_mask_fl}', '{nifti_output_file_pth}')"""
        print("Calling: ", method_call)
        left_right_registration_correction(
            sbjct_hd, tmplt_hd, nifti_input_file_pth, segment_lookup_tbl, l_r_mask,
            output_mask_fl, nifti_output_file_pth)


def correct_chirality_for_folder(nifti_input_folder_pth, images_ts_folder, nifti_output_folder):
    data_folder = '../../../../data'
    segment_lookup_tbl = os.path.join(data_folder, 'labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    nifti_input_file_pths = glob.glob(f"{nifti_input_folder_pth}/*.nii.gz")
    for nifti_input_file_pth in nifti_input_file_pths:
        filename = os.path.basename(nifti_input_file_pth)
        age_in_months = int(filename[0])
        nifti_file_extension = '.nii.gz'
        file_base_name = filename[:-len(nifti_file_extension)]
        if age_in_months == 0:
            age_in_months = 1
        sbjct_hd = os.path.join(images_ts_folder, f'{file_base_name}_0001{nifti_file_extension}')
        if not os.path.exists(sbjct_hd):
            sbjct_hd = os.path.join(images_ts_folder, f'{file_base_name}_0000{nifti_file_extension}')
        orig_chircorr_templates_folder = os.path.join(data_folder, 'orig_chircorr_templates')
        tmplt_hd = os.path.join(orig_chircorr_templates_folder, f'{str(age_in_months)}mo_T2w_acpc_dc_restore.nii.gz')
        # both the input and output masks should be left right
        l_r_mask = os.path.join(orig_chircorr_templates_folder, f'{str(age_in_months)}mo_template_LRmask.nii.gz')
        l_r_masks_folder = os.path.join(data_folder, 'LR_masks')
        if not os.path.exists(l_r_masks_folder):
            os.makedirs(l_r_masks_folder)
        output_mask_fl = os.path.join(l_r_masks_folder, f'{file_base_name}_LRmask{nifti_file_extension}')
        # the purpose here is to take the left right mask from the template and project it onto the native subject --
        # and then the chirality correction will use the subject-aligned left right mask to perform the correction
        # the aseg_mask is neither, its just a binary mask of the brain
        correct_chirality(filename, l_r_mask, nifti_input_file_pth, nifti_output_folder, output_mask_fl, sbjct_hd,
                          segment_lookup_tbl, tmplt_hd)


if __name__ == '__main__':
    nifti_input_folder_dir = sys.argv[1]
    imagesTsFolder = sys.argv[2]
    nifti_output_dir = sys.argv[3]
    correct_chirality_for_folder(nifti_input_folder_dir, imagesTsFolder, nifti_output_dir)
