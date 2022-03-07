# Author: Paul Reiners

import os
import numpy as np
import pandas as pd

from SynthSeg.dcan.look_up_tables import get_id_to_region_mapping


def generate_metrics_csv_files(results_dir, measures, mapping_file_name, alternate_mapping_file_name, labels_file_path):
    for measure in measures:
        data_file_path = os.path.join(results_dir, measure, f'{measure}.npy')
        assert os.path.exists(data_file_path)
        with open(labels_file_path) as fp:
            lines = fp.readlines()
            labels = sorted([int(line.strip()) for line in lines])
        path_segs_path = os.path.join(results_dir, 'path_segs.txt')
        with open(path_segs_path) as fp:
            lines = fp.readlines()
            paths_segs = [line.strip() for line in lines]
        data = np.load(data_file_path)
        transposed_data = data.transpose()
        id_to_region = get_id_to_region_mapping(mapping_file_name, separator=None)
        alternate_id_to_region = get_id_to_region_mapping(alternate_mapping_file_name, separator=None)
        for item in alternate_id_to_region.items():
            identifier = item[0]
            if identifier not in id_to_region.keys():
                region = item[1]
                id_to_region[identifier] = region
        regions = [id_to_region[label] for label in labels]
        df = pd.DataFrame(transposed_data, columns=regions, index=paths_segs)
        csv_file_path = os.path.join(results_dir, measure, f'{measure}.csv')
        df.to_csv(csv_file_path, index_label='subject')


if __name__ == "__main__":
    results_folder = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/'
    msrs = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    mapping_file = '../../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.md'
    alternate_mapping_file = '../../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
    generate_metrics_csv_files(results_folder, msrs, mapping_file, alternate_mapping_file)
