# Author: Paul Reiners

import os
import sys

from SynthSeg.dcan.paper.evaluate_results import get_label_list, generate_metrics_csv_files

if __name__ == "__main__":
    results_folder = sys.argv[1]
    msrs = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    mapping_file = '../../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.md'
    alternate_mapping_file = '../../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
    label_lst = \
        get_label_list(os.path.join('/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan',
                                    'labels.txt'))
    generate_metrics_csv_files(results_folder, msrs, mapping_file, alternate_mapping_file, label_lst)
