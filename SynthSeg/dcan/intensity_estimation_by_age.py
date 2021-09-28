import os.path
import sys
from os import listdir
from os.path import isfile, join
import tempfile
from shutil import copyfile

from SynthSeg.dcan.intensity_estimation import estimate_intensities


def estimate_intensities_by_age(image_dir, labels_dir, estimation_labels, result_dir):
    label_files = [f for f in listdir(labels_dir) if isfile(join(labels_dir, f))]
    image_files = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]
    ages = set([f[0] for f in label_files])
    for age in ages:
        with tempfile.TemporaryDirectory() as temp_image_dir:
            print('created temporary directory', temp_image_dir)
            for image_file in image_files:
                if image_file[0] == age:
                    copyfile(os.path.join(image_dir, image_file), os.path.join(temp_image_dir, image_file))
            with tempfile.TemporaryDirectory() as temp_labels_dir:
                print('created temporary directory', temp_labels_dir)
                for label_file in label_files:
                    if label_file[0] == age:
                        copyfile(os.path.join(labels_dir, label_file), os.path.join(temp_labels_dir, label_file))
                sub_result_dir = os.path.join(result_dir, age + "mo")
                sub_result_dir_exists = os.path.exists(sub_result_dir)
                if not sub_result_dir_exists:
                    os.makedirs(sub_result_dir)
                    print("New directory is created:", sub_result_dir)
                estimate_intensities(temp_image_dir, temp_labels_dir, estimation_labels, sub_result_dir)


if __name__ == "__main__":
    estimate_intensities_by_age(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
