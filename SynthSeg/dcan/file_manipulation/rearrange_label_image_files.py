#!/usr/bin/python

import os
import shutil
import sys


def rearrange_files(base_dir):
    nnunet_dir = '/home/feczk001/shared/data/nnUNet'

    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

    for age_dir in get_immediate_subdirectories(base_dir):
        print(age_dir)
        for subject_dir in get_immediate_subdirectories(os.path.join(base_dir, age_dir)):
            print(f'\t{subject_dir}')
            task_553_dir = os.path.join(nnunet_dir,
                                        'nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg')

            old_file_names = \
                ['aseg_acpc_final_stage5.nii.gz', f"{subject_dir}_T1w.nii.gz", f"{subject_dir}_T2w.nii.gz"]
            old_file_paths = [os.path.join(base_dir, age_dir, subject_dir, f) for f in old_file_names]
            new_file_names = \
                [f'labels/{age_dir}_{subject_dir}.nii.gz', f'images/{age_dir}_{subject_dir}_0000.nii.gz',
                 f'images/{age_dir}_{subject_dir}_0001.nii.gz']
            new_file_paths = [os.path.join(task_553_dir, f) for f in new_file_names]

            for i in range(3):
                src = old_file_paths[i]
                dst = new_file_paths[i]
                shutil.copyfile(src, dst)


if __name__ == "__main__":
    rearrange_files(sys.argv[1])
