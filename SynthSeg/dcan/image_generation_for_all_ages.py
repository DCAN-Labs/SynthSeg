import argparse
import os.path

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
    parser = argparse.ArgumentParser(
        prog='SynthSeg',
        description='Generates synthetic images from segmented images.',
        epilog="Forked off of BBillot's SynthSeg")
    parser.add_argument('input_dir', metavar='input-dir')
    parser.add_argument('output_dir', metavar='output-dir')
    parser.add_argument(
        'number_generated_images_per_real_image', metavar='number-generated-images-per-real-image', type=int)
    parser.add_argument('--starting-age-in-months', default=0, type=int)
    parser.add_argument('--distribution', default='normal',
                        help='distribution of priors (default: normal)', choices=['normal', 'uniform'])
    args = parser.parse_args()
    inpt_dr = args.input_dir
    output_dir = args.output_dir
    n = args.number_generated_images_per_real_image
    starting_age_in_months = args.starting_age_in_months
    distribution = args.distribution
    generate_images_for_all_ages(inpt_dr, output_dir, n, starting_age_in_months, prior_distribution=distribution)