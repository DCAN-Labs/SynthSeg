import ntpath
import os

import numpy as np
from tqdm import tqdm

from SynthSeg import utils
from SynthSeg.brain_generator import BrainGenerator
from SynthSeg.dcan.segmentation_common import get_generation_labels, get_priors, get_generation_classes


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_uniform_prior_means(max_min_file, age_in_months):
    data = np.load(max_min_file)
    uniform_prior_means = data[age_in_months]

    return uniform_prior_means


def get_contrast_min_max(month_data, contrast):
    contrast_data = month_data[contrast]
    if not contrast_data:
        return [0, 255]
    contrast_min = 255
    contrast_max = 0
    for k in contrast_data:
        min_max = contrast_data[k]
        if min_max[0] < contrast_min:
            contrast_min = max(0, int(min_max[0]))
        if min_max[1] > contrast_max:
            contrast_max = min(255, int(min_max[1]))

    return contrast_min, contrast_max


def generate_normal_images(
        path_label_map, priors_folder, result_dir, n_examples, downsample, age_in_months):
    """This program generates synthetic T1-weighted or T2-weighted brain MRI scans from a label map.  Specifically, it
    allows you to impose prior distributions on the GMM parameters, so that you can can generate images of desired
    intensity distribution.  You can generate images of desired contrast by imposing specified prior distributions from
    which we sample the means and standard deviations of the GMM.

    Keyword arguments:
    path_label_map -- label map to generate images from
    priors_folder -- folder containing prior_means.npy and prior_stds.npy files
    result_dir -- folder to write synthetic images to
    weighting_name -- should be either 't1' or 't2'.  Semantically, the value is immaterial---it is simply used to help
                      name the output files.
    n_examples -- number of synthetic images to generate
    """

    # general parameters
    output_shape = None  # shape of the output images, obtained by randomly cropping the generated images

    generation_labels = get_generation_labels()

    # specify structures that we want to keep in the output label maps
    output_labels = np.copy(generation_labels)

    generation_classes = get_generation_classes()

    prior_distribution, prior_means, prior_stds = get_priors(priors_folder)

    # instantiate BrainGenerator object
    brain_generator = BrainGenerator(labels_dir=path_label_map,
                                     generation_labels=generation_labels,
                                     output_labels=output_labels,
                                     generation_classes=generation_classes,
                                     prior_distributions=prior_distribution,
                                     prior_means=prior_means,
                                     prior_stds=prior_stds,
                                     output_shape=output_shape,
                                     n_channels=2,
                                     use_specific_stats_for_channel=True,
                                     downsample=downsample)

    generate_images(age_in_months, brain_generator, n_examples, result_dir)


def generate_images(age_in_months, brain_generator, n_examples, result_dir, tqdm_leave=True):
    result_dir_exists = os.path.isdir(result_dir)
    if not result_dir_exists:
        os.makedirs(result_dir)
    for n in tqdm(range(n_examples), leave=tqdm_leave):
        output_file_name = "SynthSeg_generated_{}".format(f'{n:04}')
        label_file_path = os.path.join(result_dir, 'labels', '%dmo_%s.nii.gz' % (age_in_months, output_file_name))
        if os.path.exists(label_file_path):
            continue
        # generate new image and corresponding labels
        im, lab = brain_generator.generate_brain()
        t1_im = im[:, :, :, 0]
        t2_im = im[:, :, :, 1]

        utils.save_volume(t1_im, brain_generator.aff, brain_generator.header,
                          os.path.join(
                              result_dir, 'images', '%dmo_%s_%s.nii.gz' % (age_in_months, output_file_name, '0000')))
        utils.save_volume(t2_im, brain_generator.aff, brain_generator.header,
                          os.path.join(
                              result_dir, 'images', '%dmo_%s_%s.nii.gz' % (age_in_months, output_file_name, '0001')))
        utils.save_volume(lab, brain_generator.aff, brain_generator.header,
                          label_file_path)


def generate_uniform_images(
        path_label_map, max_min_file, result_dir, n_examples, downsample, age_in_months, tqdm_leave=True):
    """This program generates synthetic T1-weighted or T2-weighted brain MRI scans from a label map.  Specifically, it
    allows you to impose prior distributions on the GMM parameters, so that you can can generate images of desired
    intensity distribution.  You can generate images of desired contrast by imposing specified prior distributions from
    which we sample the means and standard deviations of the GMM.

    Keyword arguments:
    path_label_map -- label map to generate images from
    priors_folder -- folder containing prior_means.npy and prior_stds.npy files
    result_dir -- folder to write synthetic images to
    weighting_name -- should be either 't1' or 't2'.  Semantically, the value is immaterial---it is simply used to help
                      name the output files.
    n_examples -- number of synthetic images to generate
    """

    # general parameters
    output_shape = None  # shape of the output images, obtained by randomly cropping the generated images

    generation_labels = get_generation_labels()

    # specify structures that we want to keep in the output label maps
    output_labels = np.copy(generation_labels)

    generation_classes = get_generation_classes()

    # need to give prior_means (the same applies to prior_stds) as a numpy array with K columns (the number of
    # labels) and 4 rows. The first two rows correspond to the [min, max] of the T1 contrast, and the 3rd and 4th
    # rows correspond to [min, max] of the T2 contrast.

    # prior_means is the same as I described in my previous email, but here you will need to set n_channels = 2 and
    # use_spcific_stats_for_channel = True. That will give you an image of size HxWxDx2 where the first channel will
    # correspond to the 1st and 2nd rows of prior_means, and the 2nd channel will correpsond to the 3rd and 4th rows
    # of prior_means.
    prior_means = get_uniform_prior_means(max_min_file, age_in_months)

    # instantiate BrainGenerator object
    brain_generator = BrainGenerator(labels_dir=path_label_map,
                                     generation_labels=generation_labels,
                                     output_labels=output_labels,
                                     generation_classes=generation_classes,
                                     prior_distributions='uniform',
                                     prior_means=prior_means,
                                     prior_stds=None,
                                     output_shape=output_shape,
                                     n_channels=2,
                                     use_specific_stats_for_channel=True,
                                     downsample=downsample)

    generate_images(age_in_months, brain_generator, n_examples, result_dir, tqdm_leave=tqdm_leave)
