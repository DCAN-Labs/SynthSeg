import os
import time
import ntpath
import json

import numpy as np

from SynthSeg import utils
from SynthSeg.brain_generator import BrainGenerator
from SynthSeg.dcan.segmentation_common import get_generation_labels, get_priors, get_generation_classes


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_uniform_prior_means(age_in_months):
    max_min_file = './data/labels_classes_priors/dcan/uniform/min_max_dict.json'
    f = open(max_min_file)
    data = json.load(f)
    age_in_months_str = str(age_in_months)
    if age_in_months_str in data:
        month_data = data[age_in_months_str]
        t1w_min, t1w_max = get_contrast_min_max(month_data, 'T1w')
        t2w_min, t2w_max = get_contrast_min_max(month_data, 'T2w')
        uniform_prior_means = [min(t1w_min, t2w_min), max(t1w_max, t2w_max)]
    else:
        uniform_prior_means = None
    f.close()

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


def generate_images(
        path_label_map, priors_folder, result_dir, n_examples, downsample, age_in_months, prior_distribution='uniform',
        prior_means=None, prior_stds=None):
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

    if not prior_distribution:
        prior_distribution, prior_means, prior_stds = get_priors(priors_folder)
    elif prior_distribution == 'uniform':
        prior_means = get_uniform_prior_means(age_in_months)

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

    result_dir_exists = os.path.isdir(result_dir)
    if not result_dir_exists:
        os.makedirs(result_dir)
    beginning_time = time.time()
    for n in range(n_examples):
        output_file_name = "SynthSeg_generated_{}".format(f'{n:04}')
        # save output image and label map
        full_path = os.path.join(result_dir, '%dmo_%s.nii.gz' % (age_in_months, output_file_name))
        if os.path.exists(full_path):
            continue
        # generate new image and corresponding labels
        start = time.time()
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
                          os.path.join(result_dir, 'labels', '%dmo_%s.nii.gz' % (age_in_months, output_file_name)))

        end = time.time()
        cumulative_time = end - beginning_time
        time_remaining = (n_examples - n) * cumulative_time / (n + 1)
        print(f'age: {age_in_months}; generation {n} (of {n_examples}) took {int(end - start)} seconds')
        print(f'{int(time_remaining / 60)} minutes remaining.')
