import os
import nibabel as nib

from tqdm import tqdm


def squeeze_img_data(images_dir, image_file_name):
    image_file_path = os.path.join(images_dir, image_file_name)
    image_file_img = nib.load(image_file_path)
    image_img_size = image_file_img.header.get_data_shape()
    if len(image_img_size) == 4:
        image_file_img = nib.Nifti1Image(image_file_img.get_fdata().squeeze(), image_file_img.affine)
        nib.save(image_file_img, image_file_path)
        image_file_img = nib.load(image_file_path)
    image_img_size = image_file_img.header.get_data_shape()

    return image_img_size


def main():
    task_552_dir = \
        '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg'
    labels_dir = os.path.join(task_552_dir, 'labels')
    images_dir = os.path.join(task_552_dir, 'images')
    label_files = [file for file in os.listdir(labels_dir) if os.path.isfile(os.path.join(labels_dir, file))]
    n = len(label_files)
    for i in tqdm(range(n)):
        label_file = label_files[i]
        label_img = nib.load(os.path.join(labels_dir, label_file))
        base_name = label_file[:-7]
        label_img_size = label_img.header.get_data_shape()

        t1_file_name = f'{base_name}_0000.nii.gz'
        t1_img_size = squeeze_img_data(images_dir, t1_file_name)

        t2_file_name = f'{base_name}_0001.nii.gz'
        t2_img_size = squeeze_img_data(images_dir, t2_file_name)

        if label_img_size != t1_img_size or t1_img_size != t2_img_size or label_img_size != t2_img_size:
            print(f'{label_file}:   {label_img_size}')
            print(f'{t1_file_name}: {t1_img_size}')
            print(f'{t2_file_name}: {t2_img_size}\n')


if __name__ == '__main__':
    main()
