# Author: Paul Reiners
import os
import sys

from SynthSeg.dcan.paper.append_fold_files import append_fold_files
from SynthSeg.dcan.paper.create_plots import create_cat_plots
from SynthSeg.dcan.paper.evaluate_results import evaluate_measures
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files
from SynthSeg.dcan.paper.get_all_dcan_labels import get_all_dcan_labels


def evaluate_results(result_dir, inferred_folder, labels_file_path, gt_root_dir):
    label_list = get_all_dcan_labels(labels_file_path)
    for fold_i in range(10):
        gt_dir = os.path.join(gt_root_dir, f'Fold{fold_i}/')
        seg_dir = os.path.join(inferred_folder, f'Task{516 + fold_i}_Paper_Fold{fold_i}/')
        assert os.path.exists(seg_dir)
        dir_list = os.listdir(seg_dir)
        # Ensure contains more than just plans.pkl file.
        assert len(dir_list) > 1
        summary_dir = os.path.join(result_dir, f'fold{fold_i}')
        evaluate_measures(gt_dir, seg_dir, label_list, summary_dir)


if __name__ == "__main__":
    gt_root_folder = sys.argv[1]
    inferred_dir = sys.argv[2]
    results_dir = sys.argv[3]
    dcan_folder = '/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan/'
    nnunet_dir = '/home/feczk001/shared/data/nnUNet/'
    mapping_file = os.path.join(dcan_folder, 'Freesurfer_LUT_DCAN.txt')
    evaluate_results(results_dir, inferred_dir, mapping_file, gt_root_folder)
    measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    labels = get_all_dcan_labels(mapping_file)
    for i in range(10):
        results_sub_dir = os.path.join(results_dir, f'fold{i}')
        generate_metrics_csv_files(
            results_sub_dir, measures, mapping_file)
    append_fold_files(results_dir, measures)
    create_cat_plots(results_dir, measures, False)
