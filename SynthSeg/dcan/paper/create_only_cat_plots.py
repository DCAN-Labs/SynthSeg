# Author: Paul Reiners
import argparse
import os
import shutil

import numpy as np
import pandas as pd

from SynthSeg.dcan.look_up_tables import get_id_to_region_mapping
from SynthSeg.dcan.paper.create_plots import create_cat_plots
from SynthSeg.dcan.paper.get_all_dcan_labels import get_all_dcan_labels
from SynthSeg.evaluate import evaluation


def generate_metrics_csv_files(results_dir, measures, mapping_file_name):
    path_segs_path = os.path.join(results_dir, 'path_segs.txt')
    with open(path_segs_path) as fp:
        lines = fp.readlines()
        paths_segs = [line.strip() for line in lines]
    labels_path = os.path.join(results_dir, 'labels.txt')
    with open(labels_path) as fp:
        lines = fp.readlines()
        labels = [int(line.strip()) for line in lines]
    id_to_region = get_id_to_region_mapping(mapping_file_name, separator=None)
    regions = [id_to_region[label] for label in labels]
    for measure in measures:
        data_file_path = os.path.join(results_dir, measure, f'{measure}.npy')
        assert os.path.exists(data_file_path)
        data = np.load(data_file_path)
        transposed_data = data.transpose()
        df = pd.DataFrame(transposed_data, columns=regions, index=paths_segs)
        csv_file_path = os.path.join(results_dir, measure, f'{measure}.csv')
        df.to_csv(csv_file_path, index_label='subject')


def evaluate_results(gt_dir, inferred_folder, label_list, result_dir):
    assert os.path.exists(gt_dir)
    dir_list = os.listdir(gt_dir)
    # Ensure contains more than just plans.pkl file.
    assert len(dir_list) > 0
    evaluate_measures(gt_dir, inferred_folder, label_list, result_dir)


def evaluate_measures(gt_dir, inferred_folder, label_list, result_dir):
    path_hausdorff = os.path.join(result_dir, 'hausdorff/hausdorff')
    path_hausdorff_99 = os.path.join(result_dir, 'hausdorff_99/hausdorff_99')
    path_hausdorff_95 = os.path.join(result_dir, 'hausdorff_95/hausdorff_95')
    path_mean_distance = os.path.join(result_dir, 'mean_distance/mean_distance')
    path_dice = os.path.join(result_dir, 'dice/dice')
    evaluation(gt_dir,
               inferred_folder,
               label_list, path_hausdorff=path_hausdorff, path_hausdorff_99=path_hausdorff_99,
               path_hausdorff_95=path_hausdorff_95, path_mean_distance=path_mean_distance,
               path_dice=path_dice,
               summary_dir=result_dir, crop_margin_around_gt=None)


def get_label_list(labels_file_pth):
    label_list = get_all_dcan_labels(labels_file_pth)

    return label_list


def clean_up(results_folder):
    shutil.rmtree(os.path.join(results_folder))


def create_all_cat_plots(gt_folder, inferred_dir, results_folder):
    label_list_path = os.path.join('./data/labels_classes_priors/dcan', 'Freesurfer_LUT_DCAN.txt')
    label_lst = get_label_list(label_list_path)
    evaluate_results(gt_folder, inferred_dir, label_lst, results_folder)
    metrics = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    generate_metrics_csv_files(results_folder, metrics, label_list_path)
    create_cat_plots(results_folder, metrics)
    for metric in metrics:
        folder_to_delete = os.path.join(results_folder, metric)
        clean_up(folder_to_delete)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='CreateOnlyCatPlots',
        description='Creates catplots of DICE coefficients and other stats.',
        epilog='Please contact reine097 for questions or problems in running this program.')
    parser.add_argument('gt_folder', help="Folder containing ground truth segmentations.")
    parser.add_argument('inferred_dir', help="Folder containing segmentation predictions made by model.")
    parser.add_argument('results_folder', help="Presumably empty folder where results will be written to.")
    args = parser.parse_args()
    gt_folder = args.gt_folder
    inferred_dir = args.inferred_dir
    results_folder = args.results_folder
    create_all_cat_plots(gt_folder, inferred_dir, results_folder)
