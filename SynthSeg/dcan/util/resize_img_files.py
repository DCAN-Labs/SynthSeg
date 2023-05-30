import os

import torchio as tio
from tqdm import tqdm


def resize_img_data(images_dir, image_file_name):
    # (182, 218, 182)
    image_file_path = os.path.join(images_dir, image_file_name)
    subject = tio.ScalarImage(image_file_path)
    if subject.shape != (1, 182, 218, 182):
        transform = tio.CropOrPad(
            (182, 218, 182),
        )
        transformed = transform(subject)
        transformed.save(image_file_path)


def main():
    task_552_dir = \
        '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg'
    labels_dir = os.path.join(task_552_dir, 'labels')
    images_dir = os.path.join(task_552_dir, 'images')
    label_files = [file for file in os.listdir(labels_dir) if os.path.isfile(os.path.join(labels_dir, file))]
    n = len(label_files)
    for i in tqdm(range(n)):
        label_file = label_files[i]
        resize_img_data(labels_dir, label_file)
        base_name = label_file[:-7]

        t1_file_name = f'{base_name}_0000.nii.gz'
        resize_img_data(images_dir, t1_file_name)

        t2_file_name = f'{base_name}_0001.nii.gz'
        resize_img_data(images_dir, t2_file_name)


if __name__ == '__main__':
    main()
