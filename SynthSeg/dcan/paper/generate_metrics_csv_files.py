# Author: Paul Reiners

import os
import numpy as np
import pandas as pd


def generate_metrics_csv_files():
    results_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/'
    folds = ['fold{}'.format(i) for i in range(10)]
    for fold in folds:
        measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
        for measure in measures:
            data_file_path = os.path.join(results_dir, fold, measure, f'{measure}.npy')
            if os.path.exists(data_file_path):
                labels_file_path = os.path.join(results_dir, fold, 'labels.txt')
                with open(labels_file_path) as fp:
                    lines = fp.readlines()
                    labels = [int(line.strip()) for line in lines]
                path_segs_path = os.path.join(results_dir, fold, 'path_segs.txt')
                with open(path_segs_path) as fp:
                    lines = fp.readlines()
                    paths_segs = [line.strip() for line in lines]
                data = np.load(data_file_path)
                df = pd.DataFrame(data, index=labels, columns=paths_segs)
                csv_file_path = os.path.join(results_dir, fold, measure, f'{measure}.csv')
                df.to_csv(csv_file_path)
