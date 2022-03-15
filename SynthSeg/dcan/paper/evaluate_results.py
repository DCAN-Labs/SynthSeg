# Author: Paul Reiners
import os
import sys

from SynthSeg.dcan.paper.create_plots import create_cat_plots
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files
from SynthSeg.dcan.paper.get_all_dcan_labels import get_all_dcan_labels
from SynthSeg.evaluate import evaluation


def evaluate_results(gt_dir, inferred_folder, labels_file_path, result_dir):
    label_list = get_all_dcan_labels(labels_file_path)
    assert os.path.exists(gt_dir)
    dir_list = os.listdir(gt_dir)
    # Ensure contains more than just plans.pkl file.
    assert len(dir_list) > 1
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
               summary_dir=result_dir)


if __name__ == "__main__":
    gt_folder = sys.argv[1]
    inferred_dir = sys.argv[2]
    results_dir = sys.argv[3]
    labels_file_pth = \
        os.path.join('/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan', 'labels.txt')
    evaluate_results(gt_folder, inferred_dir, labels_file_pth, results_dir)
    measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    mapping_file = '../../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.md'
    alternate_mapping_file = '../../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
    generate_metrics_csv_files(results_dir, measures, mapping_file, alternate_mapping_file, labels_file_pth)
    create_cat_plots(results_dir, measures)
