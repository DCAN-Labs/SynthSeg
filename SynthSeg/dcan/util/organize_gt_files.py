import os.path
from os import listdir
from os.path import isfile, join
from os.path import exists


gt_labels_dir = '/home/feczk001/shared/data/nnUNet/raw_data/Task516_525/gt_labels/'
nnunet_raw_data_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/'
for i in range(1, 10):
    images_ts_dir = os.path.join(nnunet_raw_data_dir, f'Task{516 + i}_Paper_Fold{i}/imagesTs/')
    only_files = [f for f in listdir(images_ts_dir) if isfile(join(images_ts_dir, f))]
    dest_dir = os.path.join(gt_labels_dir, f'Fold{i}')
    if not exists(dest_dir):
        os.mkdir(dest_dir)
    for f in only_files:
        f = f[:-len('_0000.nii.gz')] + '.nii.gz'
        src_file = os.path.join(gt_labels_dir, f)
        dest_file = os.path.join(dest_dir, f)
        if not exists(dest_file):
            os.rename(src_file, dest_file)