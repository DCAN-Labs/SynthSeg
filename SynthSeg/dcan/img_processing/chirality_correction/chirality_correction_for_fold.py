import glob
import os
from os.path import exists

from SynthSeg.dcan.img_processing.chirality_correction.left_right_registration_correction import \
    left_right_registration_correction


def correct_chirality_for_fold(fold):
    nnunet_folder = '/home/feczk001/shared/data/nnUNet/'
    paper_cross_validation_folder = 'segmentations/inferred/PaperCrossValidation/'
    nifti_input_folder_pth = os.path.join(
        nnunet_folder,
        paper_cross_validation_folder, f'original/Task{str(516 + fold)}_Paper_Fold{str(fold)}')
    data_dir = 'data'
    segment_lookup_tbl = \
        os.path.join('/home/miran045/reine097/projects/SynthSeg', data_dir,
                     'labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    nifti_input_file_pths = glob.glob(f"{nifti_input_folder_pth}/*.nii.gz")
    for nifti_input_file_pth in nifti_input_file_pths:
        filename = os.path.basename(nifti_input_file_pth)
        age_in_months = int(filename[0])
        nifti_file_extension = '.nii.gz'
        file_base_name = filename[:-len(nifti_file_extension)]
        if age_in_months == 0:
            age_in_months = 1
        sbjct_hd = \
            os.path.join(
                nnunet_folder,
                f'nnUNet_raw_data_base/nnUNet_raw_data/Task{str(516 + fold)}_Paper_Fold{str(fold)}/imagesTs',
                f'{file_base_name}_0001{nifti_file_extension}')
        tmplt_hd = \
            os.path.join(
                nnunet_folder,
                paper_cross_validation_folder, 'orig_chircorr_templates',
                f'{str(age_in_months)}mo_T2w_acpc_dc_restore.nii.gz')
        # both the input and output masks should be left right
        l_r_mask = \
            os.path.join(
                nnunet_folder,
                paper_cross_validation_folder, 'orig_chircorr_templates',
                f'{str(age_in_months)}mo_template_LRmask.nii.gz')
        output_mask_fl = os.path.join(
            nnunet_folder,
            paper_cross_validation_folder, 'LR_masks', f'{file_base_name}_LRmask{nifti_file_extension}')
        # the purpose here is to take the left right mask from the template and project it onto the native subject --
        # and then the chirality correction will use the subject-aligned left right mask to perform the correction
        # the aseg_mask is neither, its just a binary mask of the brain
        nifti_output_folder = os.path.join(
            nnunet_folder,
            paper_cross_validation_folder, f'chirality_corrected/Task{str(516 + fold)}_Paper_Fold{str(fold)}')
        is_exist = os.path.exists(nifti_output_folder)
        if not is_exist:
            os.makedirs(nifti_output_folder)
        nifti_output_file_pth = os.path.join(nifti_output_folder, filename)
        file_exists = exists(nifti_output_file_pth)
        if file_exists:
            continue
        method_call = f"""left_right_registration_correction(
            '{sbjct_hd}', '{tmplt_hd}', '{nifti_input_file_pth}', '{segment_lookup_tbl}', '{l_r_mask}', 
            '{output_mask_fl}', '{nifti_output_file_pth}')"""
        print("Calling: ", method_call)
        left_right_registration_correction(
            sbjct_hd, tmplt_hd, nifti_input_file_pth, segment_lookup_tbl, l_r_mask,
            output_mask_fl, nifti_output_file_pth)


if __name__ == '__main__':
    for fld in range(10):
        correct_chirality_for_fold(fld)
