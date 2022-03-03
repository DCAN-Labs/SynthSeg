"""
Left-right registration correction.
Usage:
  left_right_registration_correction <subject_head> <template_head> <template_mask> <nifti_input_file_path>
                                     <nifti_output_file_path> <segment_lookup_table>
  left_right_registration_correction -h | --help
Options:
  -h --help     Show this screen.
"""
import os.path
import subprocess

from SynthSeg.dcan.img_processing.correct_chirality import correct_chirality


def left_right_registration_correction(
        subject_head, template_head, nifti_input_file_path, segment_lookup_table, left_right_mask, output_mask_file,
        nifti_output_file_path):
    # 1. LR_mask_registration.sh

    # /home/miran045/reine097/projects/SynthSeg/bin/LR_mask_registration.sh
    #   /home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task516_Paper_Fold0/imagesTs/0mo_template_07_0000.nii.gz
    #   /home/miran045/reine097/projects/SynthSeg/data/sub-00006_T1w_acpc_dc_restore.nii.gz
    #   /home/miran045/reine097/projects/SynthSeg/data/sub-00006_ses-20170806_aseg_mask.nii.gz
    #   /home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/chirality_corrected/0mo_template_07_LRmask.nii.gz

    command = \
        '/home/miran045/reine097/projects/SynthSeg/bin/LR_mask_registration.sh {} {} {} {}'.format(
            subject_head, template_head, left_right_mask, output_mask_file)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return_code = process.returncode
    print(return_code)
    if return_code == 0:
        # 2. correct_chirality.py
        correct_chirality(nifti_input_file_path, segment_lookup_table, left_right_mask, nifti_output_file_path)
    else:
        msg = 'Error occurred during call to LR_mask_registration.'
        print(msg)
        raise RuntimeError(msg)


if __name__ == '__main__':
    nnunet_folder = '/home/feczk001/shared/data/nnUNet/'
    paper_cross_validation_folder = 'segmentations/inferred/PaperCrossValidation/'
    sbjct_hd = \
        os.path.join(
            nnunet_folder,
            'nnUNet_raw_data_base/nnUNet_raw_data/Task516_Paper_Fold0/imagesTs/1mo_sub-439083_0001.nii.gz')
    data_dir = '/home/miran045/reine097/projects/SynthSeg/data/'
    tmplt_hd = \
        os.path.join(
            nnunet_folder,
            paper_cross_validation_folder, 'orig_chircorr_templates/1mo_T2w_acpc_dc_restore.nii.gz')
    nifti_input_file_pth = os.path.join(
        nnunet_folder,
        paper_cross_validation_folder, 'original/Task516_Paper_Fold0/1mo_sub-439083.nii.gz')
    segment_lookup_tbl = os.path.join(data_dir, 'labels_classes_priors/dcan/FreeSurferColorLUT.txt')

    # both the input and output masks should be left right
    l_r_mask = \
        os.path.join(
            nnunet_folder,
            paper_cross_validation_folder, 'orig_chircorr_templates/1mo_template_LRmask.nii.gz')
    output_mask_fl = os.path.join(
        nnunet_folder,
        paper_cross_validation_folder, 'LR_masks/1mo_sub-439083_LRmask.nii.gz')
    # the purpose here is to take the left right mask from the template and project it onto the native subject -- and
    # then the chirality correction will use the subject-aligned left right mask to perform the correction
    # the aseg_mask is neither, its just a binary mask of the brain
    nifti_output_file_pth = os.path.join(
        nnunet_folder,
        paper_cross_validation_folder, 'chirality_corrected/Task516_Paper_Fold0/1mo_sub-439083.nii.gz')
    left_right_registration_correction(
        sbjct_hd, tmplt_hd, nifti_input_file_pth, segment_lookup_tbl, l_r_mask, output_mask_fl,
        nifti_output_file_pth)
