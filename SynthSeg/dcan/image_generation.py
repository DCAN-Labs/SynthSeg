import os
import time
import ntpath

import numpy as np

from SynthSeg import utils
from SynthSeg.brain_generator import BrainGenerator
from SynthSeg.dcan.segmentation_common import get_generation_labels, get_priors, get_generation_classes


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def generate_images(path_label_map, priors_folder, result_dir, n_examples, downsample, age_in_months):
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

    # create result dir
    utils.mkdir(result_dir)
    beginning_time = time.time()
    for n in range(n_examples):
        output_file_name = "SynthSeg_generated_{}".format(f'{n:04}')
        # save output image and label map
        full_path = os.path.join(result_dir, '%dmo_%s_%s.nii.gz' % (age_in_months, output_file_name, '0000'))
        if os.path.exists(full_path):
            continue
        # generate new image and corresponding labels
        start = time.time()
        im, lab = brain_generator.generate_brain()
        t1_im = im[:, :, :, 0]
        t2_im = im[:, :, :, 1]

        utils.save_volume(t1_im, brain_generator.aff, brain_generator.header,
                          full_path)
        utils.save_volume(t2_im, brain_generator.aff, brain_generator.header,
                          os.path.join(
                              result_dir, '%dmo_%s_%s.nii.gz' % (age_in_months, output_file_name, '0001')))
        utils.save_volume(lab, brain_generator.aff, brain_generator.header,
                          os.path.join(result_dir, '%dmo_%s.nii.gz' % (age_in_months, output_file_name)))

        end = time.time()
        cumulative_time = end - beginning_time
        time_remaining = (n_examples - n) * cumulative_time / (n + 1)
        print(f'age: {age_in_months}; generation {n} (of {n_examples}) took {int(end - start)} seconds')
        print(f'{int(time_remaining / 60)} minutes remaining.')
