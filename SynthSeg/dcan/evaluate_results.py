import os

from SynthSeg.dcan.get_all_dcan_labels import get_all_dcan_labels
from SynthSeg.evaluate import evaluation

nnunet_dir = '/home/feczk001/shared/data/nnUNet/'
mapping_file_name = '../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
result_dir = f'/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/'
labels_file_path = os.path.join(result_dir, 'labels.txt')
label_list = get_all_dcan_labels(labels_file_path)
for i in range(10):
    gt_dir = os.path.join(nnunet_dir, f'raw_data/Task516_525/gt_labels/Fold{i}/')
    seg_dir = os.path.join(nnunet_dir, f'segmentations/inferred/PaperCrossValidation/Task{516 + i}_Paper_Fold{i}/')
    if os.path.exists(seg_dir):
        summary_dir = os.path.join(result_dir, f'fold{i}')
        path_hausdorff = os.path.join(summary_dir, 'hausdorff/hausdorff')
        path_hausdorff_99 = os.path.join(summary_dir, 'hausdorff_99/hausdorff_99')
        path_hausdorff_95 = os.path.join(summary_dir, 'hausdorff_95/hausdorff_95')
        path_mean_distance = os.path.join(summary_dir, 'mean_distance/mean_distance')
        path_dice = os.path.join(summary_dir, 'dice/dice')
        evaluation(gt_dir,
                   seg_dir,
                   label_list, path_hausdorff=path_hausdorff, path_hausdorff_99=path_hausdorff_99,
                   path_hausdorff_95=path_hausdorff_95, path_mean_distance=path_mean_distance, path_dice=path_dice,
                   summary_dir=summary_dir)
