from os import listdir
from os.path import isfile, join
import shutil

mypath = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in onlyfiles:
    age = int(f[0])
    is_label_file = not f.endswith('_0000.nii.gz') and not f.endswith('_0001.nii.gz')
    if is_label_file:
        shutil.move(join(mypath, f), join(mypath, f'{age}mo', 'labels'))
