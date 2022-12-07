# /home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/labels/
# /home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/SynthSeg/
# /home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan 6 [False]
import os.path

from dcan.image_generation_from_folder import generate_images_from_folder

task_550_folder = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
for age in range(9):
    month_str = f'{age}mo'
    output_folder  = os.path.join(task_550_folder, 'SynthSeg', month_str)
    is_exist = os.path.exists(output_folder)
    if not is_exist:
        os.makedirs(output_folder)
    input_folder = os.path.join(task_550_folder, month_str, 'labels')
    priors_folder = os.path.join('./data/labels_classes_priors/dcan', month_str)
    image_count = int(10000 / 9)
    downsample = False

    generate_images_from_folder(input_folder, output_folder, priors_folder, image_count, downsample, age)
