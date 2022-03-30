import os.path

from os import listdir
from os.path import isfile, join
import nibabel as nib
import operator

from SynthSeg.dcan.look_up_tables import get_id_to_region_mapping

def count_incorrect_labels(label):
    left_thalamus_proper = 10
    ground_truth_folder = '/home/feczk001/shared/data/nnUNet/raw_data/Task516_525/gt_labels'
    inferred_folder = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/chirality_corrected'
    mislabeled_as_left_thalamus_proper = {}
    not_labeled_as_left_thalamus_proper = {}
    id_to_region_mapping = \
        get_id_to_region_mapping(
            '/home/miran045/reine097/projects/SynthSeg/data/labels_classes_priors/dcan/FreeSurferColorLUT.txt')
    for i in range(10):
        inferred_sub_folder = f'Task{str(516 + i)}_Paper_Fold{str(i)}'
        ground_truth_sub_folder = os.path.join(ground_truth_folder, f'Fold{str(i)}')
        only_files = [f for f in listdir(ground_truth_sub_folder) if isfile(join(ground_truth_sub_folder, f))]
        for f in only_files:
            ground_truth_file = os.path.join(ground_truth_sub_folder, f)
            inferred_file = os.path.join(inferred_folder, inferred_sub_folder, f)
            ground_truth_img = nib.load(ground_truth_file)
            inferred_img = nib.load(inferred_file)
            shape = ground_truth_img.shape
            ground_truth_data = ground_truth_img.get_fdata()
            inferred_data = inferred_img.get_fdata()
            for i in range(shape[0]):
                for j in range(shape[1]):
                    for k in range(shape[2]):
                        ground_truth_label = int(ground_truth_data[i][j][k])
                        inferred_label = int(inferred_data[i][j][k])
                        if inferred_label == left_thalamus_proper and ground_truth_label != left_thalamus_proper:
                            ground_truth_region = id_to_region_mapping[ground_truth_label]
                            if ground_truth_region not in mislabeled_as_left_thalamus_proper.keys():
                                mislabeled_as_left_thalamus_proper[ground_truth_region] = 1
                            else:
                                mislabeled_as_left_thalamus_proper[ground_truth_region] += 1
                        elif inferred_label != left_thalamus_proper and ground_truth_label == left_thalamus_proper:
                            inferred_region = id_to_region_mapping[inferred_label]
                            if inferred_region not in not_labeled_as_left_thalamus_proper.keys():
                                not_labeled_as_left_thalamus_proper[inferred_region] = 1
                            else:
                                not_labeled_as_left_thalamus_proper[inferred_region] += 1

    mislabeled_as_left_thalamus_proper = dict(sorted(mislabeled_as_left_thalamus_proper.items(), key=operator.itemgetter(1), reverse=True))
    print('mislabeled_as_left_thalamus_proper:', mislabeled_as_left_thalamus_proper)

    not_labeled_as_left_thalamus_proper = dict(sorted(not_labeled_as_left_thalamus_proper.items(), key=operator.itemgetter(1), reverse=True))
    print('not_labeled_as_left_thalamus_proper:', not_labeled_as_left_thalamus_proper)
