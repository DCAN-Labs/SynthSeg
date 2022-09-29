# Author: Paul Reiners

import time
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

import nibabel as nib

labels_folder = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task530_539_all/labels/'
only_files = [f for f in listdir(labels_folder) if isfile(join(labels_folder, f))]
all_labels_set = set()
i = 1
print(f'Processing {i} of 84.')
start_time = time.time()
for f in only_files:
    full_path = join(labels_folder, f)
    img = nib.load(full_path)
    image_data = img.get_fdata()
    shape = image_data.shape
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                all_labels_set.add(int(image_data[x][y][z]))
    now = time.time()
    time_per_file = (now - start_time) // i
    time_left = (84 - i) * time_per_file
    now = datetime.now()
    finish_time = now + timedelta(seconds=time_left)
    formatted_finish_time = finish_time.strftime("%H:%M:%S")
    print(f"The predicted finish time is {formatted_finish_time}")
    i += 1
all_labels_list = list(all_labels_set)
all_labels_list_sorted = sorted(all_labels_list)

labels_file = '/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan/labels2.txt'
with open(labels_file, 'w') as labels_file_handle:
    for label in all_labels_list_sorted:
        labels_file_handle.write(str(label))
        labels_file_handle.write('\n')
