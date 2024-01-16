import argparse
import os

from tqdm import tqdm

from dcan.uniform_intensity_estimation_by_age import estimate_intensities_by_age

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ten_fold_uniformity_estimation',
        description='Creates SynthSeg uniform priors for ten-fold validation.',
        epilog='Please contact reine097 for questions or problems.')
    parser.parse_args()

    for i in tqdm(range(10), desc="age loop", position=0):
        task_dir = \
            f'/scratch.global/lundq163/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task{str(540 + i)}_T1_T2_Fold{i}/'
        output_file = f'./data/labels_classes_priors/dcan/uniform/mins_maxes_fold_{i}.npy'
        if os.path.isfile(output_file):
            continue
        estimate_intensities_by_age(task_dir, output_file)
