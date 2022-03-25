import glob
import os

from SynthSeg.dcan.img_processing.chirality_correction.chirality_correction_for_folder import correct_chirality


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
        correct_chirality(filename, l_r_mask, nifti_input_file_pth, nifti_output_folder, output_mask_fl, sbjct_hd,
                          segment_lookup_tbl, tmplt_hd)


if __name__ == '__main__':
    for fld in range(10):
        correct_chirality_for_fold(fld)
