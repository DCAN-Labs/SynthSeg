import os.path
from os import listdir
from os.path import isfile, join
import shutil

base_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
t1_dir = os.path.join(base_dir, 'T1w')
t2_dir = os.path.join(base_dir, 'T2w')
label_dir = os.path.join(base_dir, 'labels')
only_files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
only_files.sort()
for i in range(len(only_files)):
    source = os.path.join(base_dir, only_files[i])
    if i % 3 == 0:
        destination = label_dir
    elif i % 3 == 1:
        destination = t1_dir
    else:
        destination = t2_dir
    shutil.move(source, destination)
