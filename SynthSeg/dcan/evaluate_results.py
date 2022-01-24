import os.path

from SynthSeg.dcan.get_all_dcan_labels import get_all_dcan_labels
from SynthSeg.evaluate import evaluation

gt_dir = '/home/feczk001/shared/data/nnUNet/raw_data/Task516_525/gt_labels/Fold0/'
seg_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/Task516_Paper_Fold0/'
mapping_file_name = '../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
label_list = get_all_dcan_labels([gt_dir, seg_dir])
summary_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/fold0'
path_hausdorff = os.path.join(summary_dir, 'hausdorff/hausdorff')
path_hausdorff_99 = os.path.join(summary_dir, 'hausdorff_99/hausdorff_99')
path_hausdorff_95 = os.path.join(summary_dir, 'hausdorff_95/hausdorff_95')
path_mean_distance = os.path.join(summary_dir, 'mean_distance/mean_distance')
path_dice = os.path.join(summary_dir, 'dice/dice')
evaluation(gt_dir,
           seg_dir,
           label_list, path_hausdorff=path_hausdorff, path_hausdorff_99=path_hausdorff_99,
           path_hausdorff_95=path_hausdorff_95, path_mean_distance=path_mean_distance, path_dice=path_dice,
           compute_score_whole_structure=True, summary_dir=summary_dir)
