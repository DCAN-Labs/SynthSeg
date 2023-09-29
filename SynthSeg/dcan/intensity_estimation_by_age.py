import argparse
import os.path

from SynthSeg.dcan.intensity_estimation import estimate_intensities


def estimate_intensities_by_age(base_dir):
    estimation_labels_file = '/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan/labels.txt'
    file1 = open(estimation_labels_file, 'r')
    lines = file1.readlines()
    labels = []
    for line in lines:
        label = int(line.strip())
        labels.append(label)
    for age in range(9):
        age_dir = f'{age}mo'
        for file_type in ['T1w', 'T2w']:
            sub_result_dir = os.path.join('./data/labels_classes_priors/dcan/normal', age_dir, file_type)
            age_path = os.path.join(base_dir, age_dir)
            image_dir = os.path.join(age_path, file_type)
            labels_dir = os.path.join(age_path, 'labels')
            estimate_intensities(image_dir, labels_dir, labels, sub_result_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='SynthSeg',
        description='Creates synthetic MRI images')
    parser.add_argument('-b', '--base_dir')
    args = parser.parse_args()
    estimate_intensities_by_age(args.base_dir)
