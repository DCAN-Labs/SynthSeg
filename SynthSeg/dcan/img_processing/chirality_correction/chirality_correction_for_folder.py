import glob
import os
from os.path import exists

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
