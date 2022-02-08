# Author: Paul Reiners

from SynthSeg.dcan.paper.evaluate_results import evaluate_results
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files

if __name__ == "__main__":
    results_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/'
    evaluate_results(results_dir)
    generate_metrics_csv_files(results_dir)
