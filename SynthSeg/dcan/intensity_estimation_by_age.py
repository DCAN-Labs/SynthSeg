import os.path

from SynthSeg.dcan.intensity_estimation import estimate_intensities


def estimate_intensities_by_age():
    estimation_labels_file = '/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan/labels.txt'
    file1 = open(estimation_labels_file, 'r')
    lines = file1.readlines()
    labels = []
    for line in lines:
        label = int(line.strip())
        labels.append(label)
    base_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
    for age in range(9):
        for file_type in ['T1w', 'T2w']:
            age_dir = f'{age}mo'
            sub_result_dir = os.path.join('./data/labels_classes_priors/dcan', age_dir, file_type)
            is_exist = os.path.exists(sub_result_dir)
            if not is_exist:
                os.makedirs(sub_result_dir)
            age_path = os.path.join(base_dir, age_dir)
            image_dir = os.path.join(age_path, file_type)
            labels_dir = os.path.join(age_path, 'labels')
            estimate_intensities(image_dir, labels_dir, labels, sub_result_dir)


if __name__ == "__main__":
    estimate_intensities_by_age()
