from os import listdir
from os.path import isfile, join
import nibabel as nib
import operator

size_to_count = dict()
base_dir = \
    '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg/' \
    'labels/'
only_files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
for f in only_files:
    img = nib.load(join(base_dir, f))
    header = img.header
    data_shape = header.get_data_shape()
    if data_shape not in size_to_count:
        size_to_count[data_shape] = 0
    size_to_count[data_shape] += 1
sorted_d = dict(sorted(size_to_count.items(), key=operator.itemgetter(1), reverse=True))
for key, value in sorted_d.items():
    print(f'{key}: {value}')
