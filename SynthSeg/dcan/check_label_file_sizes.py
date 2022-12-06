from os import listdir
from os.path import isfile, join
import nibabel as nib

base_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/labels/'
only_files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
for f in only_files:
    img = nib.load(join(base_dir, f))
    header = img.header
    print(f'{f}: {header.get_data_shape()}')
