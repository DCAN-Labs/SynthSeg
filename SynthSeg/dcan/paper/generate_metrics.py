# Author: Paul Reiners

from SynthSeg.dcan.paper.evaluate_results import evaluate_results
from SynthSeg.dcan.paper.generate_metrics_csv_files import generate_metrics_csv_files

if __name__ == "__main__":
    evaluate_results()
    generate_metrics_csv_files()
