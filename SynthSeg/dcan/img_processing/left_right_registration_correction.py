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
    sbjct_hd = \
        os.path.join(
            nnunet_folder,
            'nnUNet_raw_data_base/nnUNet_raw_data/Task516_Paper_Fold0/imagesTs/0mo_template_07_0000.nii.gz')
    data_dir = '/home/miran045/reine097/projects/SynthSeg/data/'
    tmplt_hd = os.path.join(data_dir, 'sub-00006_T1w_acpc_dc_restore.nii.gz')
    nifti_input_file_pth = os.path.join(
            nnunet_folder,
            'segmentations/inferred/PaperCrossValidation/Task516_Paper_Fold0/0mo_template_07.nii.gz')
    segment_lookup_tbl = os.path.join(data_dir, 'labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    l_r_mask = os.path.join(data_dir, 'sub-00006_ses-20170806_aseg_mask.nii.gz')
    paper_cross_validation_folder = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/'
    output_mask_fl = \
        os.path.join(paper_cross_validation_folder, 'chirality_correction_masks/0mo_template_07_LRmask.nii.gz')
    nifti_output_file_pth = \
        os.path.join(paper_cross_validation_folder, 'chirality_corrected/0mo_template_07.nii.gz')
    left_right_registration_correction(
        sbjct_hd, tmplt_hd, nifti_input_file_pth, segment_lookup_tbl, l_r_mask, output_mask_fl,
        nifti_output_file_pth)
