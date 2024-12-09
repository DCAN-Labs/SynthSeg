import argparse
from os import listdir
from os.path import isfile, join
import os.path

from tqdm import tqdm

from SynthSeg.dcan.image_generation_from_folder import generate_normal_images_from_folder, generate_uniforma_images_from_folder


def generate_normal_images_for_all_ages(input_dir, output_folder, image_count, modalities, min_age_in_months=0):
    for age in tqdm(range(min_age_in_months, 9)):
        month_str = f'{age}mo'
        input_labels_folder = os.path.join(input_dir, 'labelsTr')
        priors_folder = os.path.join('./data/labels_classes_priors/dcan/normal', month_str)
        downsample = False

        generate_normal_images_from_folder(
            input_labels_folder, output_folder, priors_folder, image_count, downsample, age, modalities)


def generate_uniform_images_for_all_ages(input_dir, priors_file, output_folder, image_count, modalities="t1t2"):
    input_labels_folder = os.path.join(input_dir, 'labelsTr')
    label_files = [f for f in listdir(input_labels_folder) if isfile(join(input_labels_folder, f))]
    ages = []
    for file_name in label_files:
        age_str = ''
        for char in file_name:
            if char.isdigit():
                age_str += char
            else:
                break
        if age_str:
            age = int(age_str)
            ages.append(age)
    for age in tqdm(ages):
        downsample = False
        generate_uniforma_images_from_folder(
            input_labels_folder, output_folder, priors_file, image_count, downsample, age, modalities, tqdm_leave=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='SynthSeg',
        description='Generates synthetic images from segmented images.',
        epilog="Please contact reine097 for questions or problems.")
    parser.add_argument('input_dir', metavar='input-dir')
    parser.add_argument('output_dir', metavar='output-dir')
    parser.add_argument('min_max_file', metavar='min-mask-file')
    parser.add_argument(
        'number_generated_images_per_age_group', metavar='number-generated-images-per-age-group', type=int)
    parser.add_argument('--modalities', default='t1t2',
                        help='which modalities to generate (default: t1t2)', choices=['t1', 't2', 't1t2'])
    #parser.add_argument('--starting-age-in-months', default=0, type=int)
    parser.add_argument('--distribution', default='normal',
                        help='distribution of priors (default: normal)', choices=['normal', 'uniform'])
    args = parser.parse_args()
    
    inpt_dr = args.input_dir
    output_dir = args.output_dir
    n = args.number_generated_images_per_age_group
    #starting_age_in_months = args.starting_age_in_months
    distribution = args.distribution
    min_max_file = args.min_max_file
    modalities = args.modalities
    generate_uniform_images_for_all_ages(inpt_dr, min_max_file, output_dir, n, modalities)
