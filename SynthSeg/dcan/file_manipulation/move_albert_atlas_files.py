import os.path
from os import listdir
from os.path import isfile, join
import shutil

shared_folder = '/home/feczk001/shared'
albert_atlas_folder = os.path.join(shared_folder, 'projects/ALBERT_atlases')
task550_folder = \
    os.path.join(shared_folder,
                 'data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg')
labels_folder = os.path.join(task550_folder, 'labels')
images_folder = os.path.join(task550_folder, 'images')

albert_atlas_files = [f for f in listdir(albert_atlas_folder) if isfile(join(albert_atlas_folder, f))]
for f in albert_atlas_files:
    if f == 'README':
        continue
    if f.endswith('_0000.nii.gz') or f.endswith('_0001.nii.gz'):
        shutil.copy(join(albert_atlas_folder, f), images_folder)
    else:
        shutil.copy(join(albert_atlas_folder, f), labels_folder)
