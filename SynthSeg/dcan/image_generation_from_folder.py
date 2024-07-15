import sys

from SynthSeg.dcan.image_generation import generate_normal_images, generate_uniform_images


def generate_normal_images_from_folder(input_folder, output_folder, priors_folder, image_count, downsample,
                                       age_in_months, modalities):
    generate_normal_images(input_folder, priors_folder, output_folder, image_count, downsample, age_in_months, modalities)


def generate_uniforma_images_from_folder(input_folder, output_folder, min_max_file, image_count, downsample,
                                         age_in_months, modalities, tqdm_leave=True):
    generate_uniform_images(
        input_folder,  min_max_file, output_folder, image_count, downsample, age_in_months, modalities, tqdm_leave=tqdm_leave)


if __name__ == "__main__":
    generate_normal_images_from_folder(
        sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] == 'True', int(sys.argv[6]))
