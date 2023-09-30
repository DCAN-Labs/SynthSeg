import os.path
import sys
from tqdm import tqdm

from dcan.image_generation_from_folder import generate_images_from_folder


def generate_images_for_all_ages(input_dir, output_folder, image_count, min_age_in_months=0,
                                 prior_distribution='normal', prior_means=None, prior_stds=None):
    for age in tqdm(range(min_age_in_months, 9)):
        month_str = f'{age}mo'
        input_labels_folder = os.path.join(input_dir, 'labelsTr')
        priors_folder = os.path.join('./data/labels_classes_priors/dcan/normal', month_str)
        downsample = False

        generate_images_from_folder(input_labels_folder, output_folder, priors_folder, image_count, downsample, age,
                                    prior_distribution, prior_means, prior_stds)


if __name__ == "__main__":
    inpt_dr = sys.argv[1]
    output_dir = sys.argv[2]
    n = int(sys.argv[3])
    if len(sys.argv) == 4:
        generate_images_for_all_ages(inpt_dr, output_dir, n, 0)
    else:
        generate_images_for_all_ages(inpt_dr, output_dir, n, int(sys.argv[3]))
