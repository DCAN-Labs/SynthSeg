import argparse
import os.path
import statistics
from os import listdir
from os.path import isfile, join

import nibabel as nib
import numpy as np


def compute_metrics(y_true, y_pred):
    """
    Computes IOU and Dice Score.

    Args:
      y_true (tensor) - ground truth label map
      y_pred (tensor) - predicted label map
    """

    smoothening_factor = 0.00001

    intersection = 0.0
    combined_area = 0.0
    for i in range(1, 163):
        intersection += np.sum((y_pred == i) * (y_true == i))
        y_true_area = np.sum((y_true == i))
        y_pred_area = np.sum((y_pred == i))
        combined_area += y_true_area + y_pred_area

    iou = (intersection + smoothening_factor) / (combined_area - intersection + smoothening_factor)

    dice_score = 2 * ((intersection + smoothening_factor) / (combined_area + smoothening_factor))

    return iou, dice_score

def get_medians(ground_truth_folder, predictions_folder, month=None):
    if month is not None:
        ground_truth_folder = os.path.join(ground_truth_folder, f'{month}mo')
        predictions_folder = os.path.join(predictions_folder, f'{month}mo')
    gt_files = [f for f in listdir(ground_truth_folder) if isfile(join(ground_truth_folder, f))]

    ious = []
    dice_scores = []
    for gt_file in gt_files:
        gt_file_path = os.path.join(ground_truth_folder, gt_file)
        gt_img = nib.load(gt_file_path)
        gt_image_data = gt_img.get_fdata()
        gt_image_data_int = gt_image_data.astype(int)
        gt_image_data_int_1d = gt_image_data_int.ravel()
        pred_file_path = os.path.join(predictions_folder, gt_file)
        pred_img = nib.load(pred_file_path)
        pred_image_data = pred_img.get_fdata()
        pred_image_data_int = pred_image_data.astype(int)
        y_pred_1d = pred_image_data_int.ravel()
        the_iou, the_dice_score = compute_metrics(gt_image_data_int_1d, y_pred_1d)
        ious.append(the_iou)
        dice_scores.append(the_dice_score)
        print(f'subject: {gt_file}')
        print(f'\tiou:        {the_iou}')
        print(f'\tdice_score: {the_dice_score}')
    iou_median = statistics.median(ious)
    dice_score_median = statistics.median(dice_scores)

    return {'iou_median': iou_median, 'dice_score_median': dice_score_median, "count": len(ious)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='IOUDiceScore',
        description='Computes IOU and DICE statistics for a pair of sets of files',
        epilog='Pleae contact reine097 if you have questions or run into problems.')
    parser.add_argument('ground_truth_folder', help="The folder containing the ground truth segmentations.")
    parser.add_argument('predictions_folder',
                        help="The folder of segmentations whose accuracy is to be measured.  \
                        These will typically be the predictions of a segmentation model.")
    args = parser.parse_args()
    ground_truth_folder = args.ground_truth_folder
    predictions_folder = args.predictions_folder
    print()
    medians = get_medians(ground_truth_folder, predictions_folder)
    print(f'iou_median: {medians["iou_median"]}')
    print(f'dice_score_median: {medians["dice_score_median"]}')
