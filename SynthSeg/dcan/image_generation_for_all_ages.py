# /home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/labels/
# /home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/SynthSeg/
# /home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan 6 [False]
import os.path
import sys

from dcan.image_generation_from_folder import generate_images_from_folder


def generate_images_for_all_ages(task_folder, image_count, min_age_in_months=0,
                                 prior_distribution='uniform', prior_means=None, prior_stds=None):
    for age in range(min_age_in_months, 9):
        month_str = f'{age}mo'
        output_folder = task_folder
        is_exist = output_folder
        if not is_exist:
            os.makedirs(output_folder)
        input_folder = os.path.join(task_folder, 'labels')
        priors_folder = os.path.join('./data/labels_classes_priors/dcan', month_str)
        downsample = False

        generate_images_from_folder(input_folder, output_folder, priors_folder, image_count, downsample, age,
                                    prior_distribution, prior_means, prior_stds)


if __name__ == "__main__":
    task_dir = sys.argv[1]
    n = int(sys.argv[2])
    if len(sys.argv) == 3:
        generate_images_for_all_ages(task_dir, n, 0)
    else:
        generate_images_for_all_ages(task_dir, n, int(sys.argv[3]))
