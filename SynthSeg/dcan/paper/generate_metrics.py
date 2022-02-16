# Author: Paul Reiners
import sys

from SynthSeg.dcan.paper.append_fold_files import append_fold_files
from SynthSeg.dcan.paper.create_plots import create_box_plots, create_cat_plots
from SynthSeg.dcan.paper.evaluate_results import evaluate_results
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files

if __name__ == "__main__":
    results_dir = sys.argv[1]
    evaluate_results(results_dir)
    measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    mapping_file = '../../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.md'
    alternate_mapping_file = '../../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
    generate_metrics_csv_files(results_dir, measures, mapping_file, alternate_mapping_file)
    append_fold_files(results_dir, measures)
    create_box_plots(results_dir, measures)
    create_cat_plots(results_dir, measures)
