import argparse
import os

from tqdm import tqdm

from SynthSeg.dcan.uniform_intensity_estimation_by_age import estimate_intensities_by_age

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ten_fold_uniformity_estimation',
        description='Creates SynthSeg uniform priors for ten-fold validation.',
        epilog='Please contact reine097 for questions or problems.')
    parser.add_argument('task_dir')
    parser.add_argument('output_file')
    args = parser.parse_args()
    
    task_dir = args.task_dir
    output_file = args.output_file

    if not os.path.isfile(output_file):
        estimate_intensities_by_age(task_dir, output_file)