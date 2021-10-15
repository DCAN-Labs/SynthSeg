import sys
from os import listdir
from os.path import isfile, join

from SynthSeg.dcan.image_generation import generate_images


def generate_images_from_folder(input_folder, output_folder, priors_folder, image_count):
    only_files = [f for f in listdir(input_folder) if isfile(join(input_folder, f))]
    total_image_count = len(only_files) * image_count
    generate_images(input_folder, priors_folder, output_folder, total_image_count)


if __name__ == "__main__":
    generate_images_from_folder(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
