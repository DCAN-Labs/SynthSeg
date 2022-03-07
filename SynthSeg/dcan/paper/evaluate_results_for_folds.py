# Author: Paul Reiners
import os
import sys

from SynthSeg.dcan.paper.append_fold_files import append_fold_files
from SynthSeg.dcan.paper.create_plots import create_box_plots, create_cat_plots
from SynthSeg.dcan.paper.evaluate_results import evaluate_measures
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files
from SynthSeg.dcan.paper.get_all_dcan_labels import get_all_dcan_labels


def evaluate_results(result_dir, inferred_folder):
    nnunet_dir = '/home/feczk001/shared/data/nnUNet/'
    labels_file_path = os.path.join(result_dir, 'labels.txt')
    label_list = get_all_dcan_labels(labels_file_path)
    for i in range(10):
        gt_dir = os.path.join(nnunet_dir, f'raw_data/Task516_525/gt_labels/Fold{i}/')
        seg_dir = os.path.join(inferred_folder, f'Task{516 + i}_Paper_Fold{i}/')
        if os.path.exists(seg_dir):
            dir_list = os.listdir(seg_dir)
            # Ensure contains more than just plans.pkl file.
            if len(dir_list) > 1:
                summary_dir = os.path.join(result_dir, f'fold{i}')
                evaluate_measures(gt_dir, seg_dir, label_list, summary_dir)


if __name__ == "__main__":
    inferred_dir = sys.argv[1]
    results_dir = sys.argv[2]
    evaluate_results(results_dir, inferred_dir)
    measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    mapping_file = '../../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.md'
    alternate_mapping_file = '../../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
    generate_metrics_csv_files(results_dir, measures, mapping_file, alternate_mapping_file)
    append_fold_files(results_dir, measures)
    create_box_plots(results_dir, measures)
    create_cat_plots(results_dir, measures)
