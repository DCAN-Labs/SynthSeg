import sys
from os import listdir
from os.path import isfile, join

from SynthSeg.dcan.image_generation import generate_images


def generate_images_from_folder(input_folder, output_folder, priors_folder, image_count, downsample, age_in_months):
    generate_images(input_folder, priors_folder, output_folder, image_count, downsample, age_in_months)


if __name__ == "__main__":
    generate_images_from_folder(
        sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] == 'True', int(sys.argv[6]))
