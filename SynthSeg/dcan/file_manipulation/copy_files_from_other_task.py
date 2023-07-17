import os.path
from os import listdir
from os.path import isfile, join
import shutil

nnunet_raw_data_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data'
base_src_dir = os.path.join(nnunet_raw_data_dir, 'Task553_uniform_distribution_synthseg')
dest_dir = os.path.join(nnunet_raw_data_dir, 'Task554_uniform_distribution_synth_set_no_flipping')
src_sub_dirs = ['imagesTr', 'imagesTs', 'labelsTr', 'labelsTs']
for src_sub_dir in src_sub_dirs:
    complete_src_sub_dir = os.path.join(base_src_dir, src_sub_dir)
    complete_dst_sub_dir = os.path.join(dest_dir, src_sub_dir)
    if not os.path.exists(complete_dst_sub_dir):
        os.makedirs(complete_dst_sub_dir)
    only_files = [f for f in listdir(complete_src_sub_dir) if isfile(join(complete_src_sub_dir, f))]
    for f in only_files:
        if 'SynthSeg' not in f:
            shutil.copy(os.path.join(complete_src_sub_dir, f), complete_dst_sub_dir)
