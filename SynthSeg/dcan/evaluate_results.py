from SynthSeg.dcan.get_all_dcan_labels import get_all_dcan_labels
from SynthSeg.dcan.look_up_tables import get_ids
from SynthSeg.evaluate import evaluation

gt_dir = '/home/feczk001/shared/data/nnUNet/raw_data/Task516_525/gt_labels/Fold0/'
seg_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/Task516_Paper_Fold0/'
mapping_file_name = '../../data/labels_classes_priors/dcan/FreeSurferColorLUT.txt'
label_list = get_all_dcan_labels([gt_dir, seg_dir])
path_hausdorff = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/hausdorff/'
path_hausdorff_99 = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/hausdorff_99/'
path_hausdorff_95 = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/hausdorff_95/'
path_mean_distance = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/mean_distance/'

evaluation(gt_dir,
               seg_dir,
               label_list, path_hausdorff=path_hausdorff, path_hausdorff_99=path_hausdorff_99,
           path_hausdorff_95=path_hausdorff_95, path_mean_distance=path_mean_distance)