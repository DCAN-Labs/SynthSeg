# python imports
import os
import numpy as np
from scipy.stats import wilcoxon
from scipy.ndimage.morphology import distance_transform_edt

# third-party imports
from ext.lab2im import utils
from ext.lab2im import edit_volumes


def fast_dice(x, y, labels):
    """Fast implementation of Dice scores.
    :param x: input label map
    :param y: input label map of the same size as x
    :param labels: numpy array of labels to evaluate on
    :return: numpy array with Dice scores in the same order as labels.
    """

    assert x.shape == y.shape, 'both inputs should have same size, had {} and {}'.format(x.shape, y.shape)

    if len(labels) > 1:
        # sort labels
        labels_sorted = np.sort(labels)

        # build bins for histograms
        label_edges = np.sort(np.concatenate([labels_sorted - 0.1, labels_sorted + 0.1]))
        label_edges = np.insert(label_edges, [0, len(label_edges)], [labels_sorted[0] - 100, labels_sorted[-1] + 100])

        # compute Dice and re-arange scores in initial order
        hst = np.histogram2d(x.flatten(), y.flatten(), bins=label_edges)[0]
        idx = np.arange(start=1, stop=2 * len(labels_sorted), step=2)
        dice_score = 2 * np.diag(hst)[idx] / (np.sum(hst, 0)[idx] + np.sum(hst, 1)[idx] + 1e-5)
        dice_score = dice_score[np.searchsorted(labels_sorted, labels)]

    else:
        dice_score = dice(x == labels[0], y == labels[0])

    return dice_score


def dice(x, y):
    """Implementation of dice scores ofr 0/1 numy array"""
    return 2 * np.sum(x * y) / (np.sum(x) + np.sum(y))


def surface_distances(x, y, hausdorff_percentile=None, return_coordinate_max_distance=False):
    """Computes the maximum boundary distance (Haussdorff distance), and the average boundary distance of two masks.
    :param x: numpy array (boolean or 0/1)
    :param y: numpy array (boolean or 0/1)
    :param hausdorff_percentile: (optional) percentile (from 0 to 100) for which to compute the Hausdorff distance.
    Set this to 100 to compute the real Hausdorff distance (default). Can also be a list, where HD will be compute for
    the provided values.
    :param return_coordinate_max_distance: (optional) when set to true, the function will return the coordinates of the
    voxel with the highest distance (only if hausdorff_percentile=100).
    :return: max_dist, mean_dist(, coordinate_max_distance)
    max_dist: scalar with HD computed for the given percentile (or list if hausdorff_percentile was given as a list).
    mean_dist: scalar with average surface distance
    coordinate_max_distance: only returned return_coordinate_max_distance is True."""

    assert x.shape == y.shape, 'both inputs should have same size, had {} and {}'.format(x.shape, y.shape)
    n_dims = len(x.shape)

    hausdorff_percentile = 100 if hausdorff_percentile is None else hausdorff_percentile
    hausdorff_percentile = utils.reformat_to_list(hausdorff_percentile)

    # crop x and y around ROI
    _, crop_x = edit_volumes.crop_volume_around_region(x)
    _, crop_y = edit_volumes.crop_volume_around_region(y)

    # set distances to maximum volume shape if they are not defined
    if (crop_x is None) | (crop_y is None):
        return max(x.shape), max(x.shape)

    crop = np.concatenate([np.minimum(crop_x, crop_y)[:n_dims], np.maximum(crop_x, crop_y)[n_dims:]])
    x = edit_volumes.crop_volume_with_idx(x, crop)
    y = edit_volumes.crop_volume_with_idx(y, crop)

    # detect edge
    x_dist_int = distance_transform_edt(x * 1)
    x_edge = (x_dist_int == 1) * 1
    y_dist_int = distance_transform_edt(y * 1)
    y_edge = (y_dist_int == 1) * 1

    # calculate distance from edge
    x_dist = distance_transform_edt(np.logical_not(x_edge))
    y_dist = distance_transform_edt(np.logical_not(y_edge))

    # find distances from the 2 surfaces
    x_dists_to_y = y_dist[x_edge == 1]
    y_dists_to_x = x_dist[y_edge == 1]

    max_dist = list()
    coordinate_max_distance = None
    for hd_percentile in hausdorff_percentile:

        # find max distance from the 2 surfaces
        if hd_percentile == 100:
            max_dist.append(np.max(np.concatenate([x_dists_to_y, y_dists_to_x])))

            if return_coordinate_max_distance:
                indices_x_surface = np.where(x_edge == 1)
                idx_max_distance_x = np.where(x_dists_to_y == max_dist)[0]
                if idx_max_distance_x.size != 0:
                    coordinate_max_distance = np.stack(indices_x_surface).transpose()[idx_max_distance_x]
                else:
                    indices_y_surface = np.where(y_edge == 1)
                    idx_max_distance_y = np.where(y_dists_to_x == max_dist)[0]
                    coordinate_max_distance = np.stack(indices_y_surface).transpose()[idx_max_distance_y]

        # find percentile of max distance
        else:
            max_dist.append(np.percentile(np.concatenate([x_dists_to_y, y_dists_to_x]), hd_percentile))

    # find average distance between 2 surfaces
    if x_dists_to_y.shape[0] > 0:
        x_mean_dist_to_y = np.mean(x_dists_to_y)
    else:
        x_mean_dist_to_y = max(x.shape)
    if y_dists_to_x.shape[0] > 0:
        y_mean_dist_to_x = np.mean(y_dists_to_x)
    else:
        y_mean_dist_to_x = max(x.shape)
    mean_dist = (x_mean_dist_to_y + y_mean_dist_to_x) / 2

    # convert max dist back to scalar if HD only computed for 1 percentile
    if len(max_dist) == 1:
        max_dist = max_dist[0]

    # return coordinate of max distance if necessary
    if coordinate_max_distance is not None:
        return max_dist, mean_dist, coordinate_max_distance
    else:
        return max_dist, mean_dist


def compute_non_parametric_paired_test(dice_ref, dice_compare, eval_indices=None, alternative='two-sided'):
    """Compute non-parametric paired t-tests between two sets of Dice scores.
    :param dice_ref: numpy array with Dice scores, rows represent structures, and columns represent subjects.
    Taken as reference for one-sided tests.
    :param dice_compare: numpy array of the same format as dice_ref.
    :param eval_indices: (optional) list or 1d array indicating the row indices of structures to run the tests for.
    Default is None, for which p-values are computed for all rows.
    :param alternative: (optional) The alternative hypothesis to be tested, Cab be 'two-sided', 'greater', 'less'.
    :return: 1d numpy array, with p-values for all tests on evaluated structures, as well as an additionnal test for
    average scores (last value of the array). The average score is computed only on the evaluation structures.
    """

    # take all rows if indices not specified
    if eval_indices is None:
        if len(dice_ref.shape) > 1:
            eval_indices = np.arange(dice_ref.shape[0])
        else:
            eval_indices = []

    # loop over all evaluation label values
    pvalues = list()
    if len(eval_indices) > 1:
        for idx in eval_indices:

            x = dice_ref[idx, :]
            y = dice_compare[idx, :]
            _, p = wilcoxon(x, y, alternative=alternative)
            pvalues.append(p)

        # average score
        x = np.mean(dice_ref[eval_indices, :], axis=0)
        y = np.mean(dice_compare[eval_indices, :], axis=0)
        _, p = wilcoxon(x, y, alternative=alternative)
        pvalues.append(p)

    else:
        # average score
        _, p = wilcoxon(dice_ref, dice_compare, alternative=alternative)
        pvalues.append(p)

    return np.array(pvalues)


def cohens_d(volumes_x, volumes_y):

    means_x = np.mean(volumes_x, axis=0)
    means_y = np.mean(volumes_y, axis=0)

    var_x = np.var(volumes_x, axis=0)
    var_y = np.var(volumes_y, axis=0)

    n_x = np.shape(volumes_x)[0]
    n_y = np.shape(volumes_y)[0]

    std = np.sqrt(((n_x-1)*var_x + (n_y-1)*var_y) / (n_x + n_y - 2))
    cohensd = (means_x - means_y) / std

    return cohensd


def evaluation(gt_dir,
               seg_dir,
               label_list,
               mask_dir=None,
               compute_score_whole_structure=False,
               path_dice=None,
               path_hausdorff=None,
               path_hausdorff_99=None,
               path_hausdorff_95=None,
               path_mean_distance=None,
               crop_margin_around_gt=10,
               list_incorrect_labels=None,
               list_correct_labels=None,
               use_nearest_label=False,
               recompute=True,
               verbose=True,
               summary_dir=None):
    """This function computes Dice scores, as well as surface distances, between two sets of labels maps in gt_dir
    (ground truth) and seg_dir (typically predictions). Labels maps in both folders are matched by sorting order.
    :param gt_dir: path of directory with gt label maps
    :param seg_dir: path of directory with label maps to compare to gt_dir. Matched to gt label maps by sorting order.
    :param label_list: list of label values for which to compute evaluation metrics. Can be a sequence, a 1d numpy
    array, or the path to such array.
    :param compute_score_whole_structure: (optional) whether to also compute the selected scores for the whole segmented
    structure (i.e. scores are computed for a single structure obtained by regrouping all non-zero values). If True, the
    resulting scores are added as an extra row to the result matrices. Default is False.
    :param path_dice: path where the resulting Dice will be writen as numpy array.
    Default is None, where the array is not saved.
    :param path_hausdorff: path where the resulting Hausdorff distances will be writen as numpy array (only if
    compute_distances is True). Default is None, where the array is not saved.
    :param path_mean_distance: path where the resulting mean distances will be writen as numpy array (only if
    compute_distances is True). Default is None, where the array is not saved.
    :param crop_margin_around_gt: (optional) margin by which to crop around the gt volumes, in order to copute the
    scores more efficiently. If None, no cropping is performed.
    :param recompute: (optional) whether to recompute the already existing results. Default is True.
    :param verbose: (optional) whether to print out info about the remaining number of cases.
    :return: numpy array containing all Dice scores (rows=ROIs in the same order as they appear in label_list,
    columns=subjects sorted by their names in alphabetical order). Also returns numpy arrays for Hausdorff and mean
    distances if compute_distances is True (same structure as the Dice result matrix).
    """

    # check whether to recompute
    compute_dice = not os.path.isfile(path_dice) if (path_dice is not None) else True
    compute_hausdorff = not os.path.isfile(path_hausdorff) if (path_hausdorff is not None) else False
    compute_hausdorff_99 = not os.path.isfile(path_hausdorff_99) if (path_hausdorff_99 is not None) else False
    compute_hausdorff_95 = not os.path.isfile(path_hausdorff_95) if (path_hausdorff_95 is not None) else False
    compute_mean_dist = not os.path.isfile(path_mean_distance) if (path_mean_distance is not None) else False
    compute_hd = [compute_hausdorff, compute_hausdorff_99, compute_hausdorff_95]

    if compute_dice | any(compute_hd) | compute_mean_dist | recompute:

        # get list label maps to compare
        path_gt_labels = utils.list_images_in_folder(gt_dir)
        path_segs = utils.list_images_in_folder(seg_dir)
        path_gt_labels = utils.reformat_to_list(path_gt_labels, length=len(path_segs))
        if len(path_gt_labels) != len(path_segs):
            print('gt and segmentation folders must have the same amount of label maps.')
        if mask_dir is not None:
            path_masks = utils.list_images_in_folder(mask_dir)
            if len(path_masks) != len(path_segs):
                print('not the same amount of masks and segmentations.')
        else:
            path_masks = [None] * len(path_segs)

        # load labels list
        label_list, _ = utils.get_list_labels(label_list=label_list, FS_sort=True, labels_dir=gt_dir)
        n_labels = len(label_list)
        max_label = np.max(label_list) + 1

        if summary_dir:
            if not os.path.exists(summary_dir):
                os.makedirs(summary_dir)
            labels_file = os.path.join(summary_dir, "labels.txt")
            label_list_file = open(labels_file, 'w')
            for element in label_list:
                label_list_file.write(str(element) + '\n')
            label_list_file.close()
            textfile = open(os.path.join(summary_dir, "path_segs.txt"), "w")
            for element in path_segs:
                base_name = os.path.basename(element)
                textfile.write(base_name + "\n")
            textfile.close()

        # initialise result matrices
        if compute_score_whole_structure:
            max_dists = np.zeros((n_labels + 1, len(path_segs), 3))
            mean_dists = np.zeros((n_labels + 1, len(path_segs)))
            dice_coefs = np.zeros((n_labels + 1, len(path_segs)))
        else:
            max_dists = np.zeros((n_labels, len(path_segs), 3))
            mean_dists = np.zeros((n_labels, len(path_segs)))
            dice_coefs = np.zeros((n_labels, len(path_segs)))

        # loop over segmentations
        loop_info = utils.LoopInfo(len(path_segs), 10, 'evaluating', print_time=True)
        for idx, (path_gt, path_seg, path_mask) in enumerate(zip(path_gt_labels, path_segs, path_masks)):
            if verbose:
                loop_info.update(idx)

            # load gt labels and segmentation
            gt_labels = utils.load_volume(path_gt, dtype='int')
            seg = utils.load_volume(path_seg, dtype='int')
            if path_mask is not None:
                mask = utils.load_volume(path_mask, dtype='bool')
                gt_labels[mask] = max_label
                seg[mask] = max_label

            # crop images
            if crop_margin_around_gt is not None:
                gt_labels, cropping = edit_volumes.crop_volume_around_region(gt_labels, margin=crop_margin_around_gt)
                seg = edit_volumes.crop_volume_with_idx(seg, cropping)

            if list_incorrect_labels is not None:
                seg = edit_volumes.correct_label_map(seg, list_incorrect_labels, list_correct_labels, use_nearest_label)

            # compute Dice scores
            dice_coefs[:n_labels, idx] = fast_dice(gt_labels, seg, label_list)

            # compute Dice scores for whole structures
            if compute_score_whole_structure:
                temp_gt = (gt_labels > 0) * 1
                temp_seg = (seg > 0) * 1
                dice_coefs[-1, idx] = dice(temp_gt, temp_seg)
            else:
                temp_gt = temp_seg = None

            # compute average and Hausdorff distances
            if any(compute_hd) | compute_mean_dist:

                # compute unique label values
                unique_gt_labels = np.unique(gt_labels)
                unique_seg_labels = np.unique(seg)

                # compute max/mean surface distances for all labels
                for index, label in enumerate(label_list):
                    if (label in unique_gt_labels) & (label in unique_seg_labels):
                        mask_gt = np.where(gt_labels == label, True, False)
                        mask_seg = np.where(seg == label, True, False)
                        tmp_max_dists, mean_dists[index, idx] = surface_distances(mask_gt, mask_seg, [100, 99, 95])
                        max_dists[index, idx, :] = np.array(tmp_max_dists)
                    else:
                        mean_dists[index, idx] = max(gt_labels.shape)
                        max_dists[index, idx, :] = np.array([max(gt_labels.shape)] * 3)

                # compute max/mean distances for whole structure
                if compute_score_whole_structure:
                    tmp_max_dists, mean_dists[-1, idx] = surface_distances(temp_gt, temp_seg, [100, 99, 95])
                    max_dists[-1, idx, :] = np.array(tmp_max_dists)

        # write results
        if path_dice is not None:
            utils.mkdir(os.path.dirname(path_dice))
            np.save(path_dice, dice_coefs)
        if path_hausdorff is not None:
            utils.mkdir(os.path.dirname(path_hausdorff))
            np.save(path_hausdorff, max_dists[..., 0])
        if path_hausdorff_99 is not None:
            utils.mkdir(os.path.dirname(path_hausdorff_99))
            np.save(path_hausdorff_99, max_dists[..., 1])
        if path_hausdorff_95 is not None:
            utils.mkdir(os.path.dirname(path_hausdorff_95))
            np.save(path_hausdorff_95, max_dists[..., 2])
        if path_mean_distance is not None:
            utils.mkdir(os.path.dirname(path_mean_distance))
            np.save(path_mean_distance, max_dists[..., 2])
