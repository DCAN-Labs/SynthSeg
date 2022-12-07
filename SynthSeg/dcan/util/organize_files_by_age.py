import os
import shutil
from os import listdir
from os.path import isfile, join

base_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
for age in range(9):
    age_dir = os.path.join(base_dir, f'{age}mo')
    for folder in ['labels', 'T1w', 'T2w']:
        age_type_dir = os.path.join(age_dir, folder)
        is_exist = os.path.exists(age_type_dir)
        if not is_exist:
            os.makedirs(age_type_dir)
for folder in ['labels', 'T1w', 'T2w']:
    src_dir = os.path.join(base_dir, folder)
    only_files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
    for f in only_files:
        dest_age_dir = f[:3]
        dest_dir = os.path.join(base_dir, dest_age_dir, folder)
        source_file = join(src_dir, f)
        shutil.move(source_file, dest_dir)
