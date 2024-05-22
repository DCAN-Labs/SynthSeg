import os
import sys

from dcan.paper.create_plots import create_cat_plots
from dcan.paper.evaluate_results import get_label_list, evaluate_results, generate_metrics_csv_files

if __name__ == "__main__":
    age_in_months = int(sys.argv[1])
    gt_folder = os.path.join(sys.argv[2], f'{age_in_months}mo')
    inferred_dir = os.path.join(sys.argv[3], f'{age_in_months}mo')
    results_folder = os.path.join(sys.argv[4], f'{age_in_months}mo', 'img')
    label_list_path = os.path.join('../../../data/labels_classes_priors/dcan', 'Freesurfer_LUT_DCAN.txt')
    label_lst = get_label_list(label_list_path)
    evaluate_results(gt_folder, inferred_dir, label_lst, results_folder)
    metrics = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    mapping_file = '../../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.txt'
    generate_metrics_csv_files(results_folder, metrics, label_list_path)
    create_cat_plots(os.path.join(results_folder), metrics)
