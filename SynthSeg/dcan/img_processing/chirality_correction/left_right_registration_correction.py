import subprocess

from SynthSeg.dcan.img_processing.chirality_correction.dilate_LRmask import dilate_lr_mask
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
        command = f'dilate_lr_mask({output_mask_file}, {left_right_mask})'
        print(f"Command: {command}")
        dilate_lr_mask(output_mask_file, left_right_mask)
        # 2. correct_chirality.py
        correct_chirality(nifti_input_file_path, segment_lookup_table, left_right_mask, nifti_output_file_path)
    else:
        msg = 'Error occurred during call to LR_mask_registration.'
        print(msg)
