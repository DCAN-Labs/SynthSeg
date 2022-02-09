# Author: Paul Reiners
from SynthSeg.dcan.paper.append_fold_files import append_fold_files
from SynthSeg.dcan.paper.create_plots import create_violin_plots
from SynthSeg.dcan.paper.evaluate_results import evaluate_results
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files

if __name__ == "__main__":
    results_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/'
    evaluate_results(results_dir)
    measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    generate_metrics_csv_files(results_dir, measures)
    append_fold_files(results_dir, measures)
    create_violin_plots(results_dir, measures)
