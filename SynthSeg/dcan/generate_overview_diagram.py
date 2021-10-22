import os

import numpy as np

from SynthSeg import utils
from SynthSeg.brain_generator import BrainGenerator
from SynthSeg.dcan.segmentation_common import get_generation_labels, get_generation_classes, get_priors
from ext.lab2im.utils import mkdir


def generate_overview_diagram(path_label_map, priors_dir, result_dir):
    # general parameters
    output_shape = None  # shape of the output images, obtained by randomly cropping the generated images

    generation_labels = get_generation_labels()

    # specify structures that we want to keep in the output label maps
    output_labels = np.copy(generation_labels)

    generation_classes = get_generation_classes()

    prior_distribution, prior_means, prior_stds = get_priors(priors_dir)

    # create result dir
    utils.mkdir(result_dir)

    create_image_files(generation_classes, generation_labels, output_labels, output_shape, path_label_map,
                       prior_distribution, prior_means, prior_stds, result_dir, "SynthSeg_generated_gmm_sampling")
    create_image_files(generation_classes, generation_labels, output_labels, output_shape, path_label_map,
                       prior_distribution, prior_means, prior_stds, result_dir, "SynthSeg_generated_bias_field",
                       bias_field_std=.5,
                       bias_shape_factor=.025)
    create_image_files(generation_classes, generation_labels, output_labels, output_shape, path_label_map,
                       prior_distribution, prior_means, prior_stds, result_dir, "SynthSeg_generated_downsampling",
                       downsample=True)


def create_image_files(generation_classes, generation_labels, output_labels, output_shape, path_label_map,
                       prior_distribution, prior_means, prior_stds, result_dir, output_file_name,
                       blur_range=None,
                       bias_field_std=0.0,
                       bias_shape_factor=0.0,
                       downsample=False):
    # instantiate BrainGenerator object
    brain_generator_gmm_sampling = BrainGenerator(labels_dir=path_label_map,
                                                  generation_labels=generation_labels,
                                                  output_labels=output_labels,
                                                  generation_classes=generation_classes,
                                                  prior_distributions=prior_distribution,
                                                  prior_means=prior_means,
                                                  prior_stds=prior_stds,
                                                  output_shape=output_shape,
                                                  n_channels=2,
                                                  use_specific_stats_for_channel=True,
                                                  blur_range=blur_range,
                                                  bias_field_std=bias_field_std,
                                                  bias_shape_factor=bias_shape_factor,
                                                  downsample=downsample)
    # generate new image and corresponding labels
    im, lab = brain_generator_gmm_sampling.generate_brain()
    t1_im = im[:, :, :, 0]
    t2_im = im[:, :, :, 1]
    # save output image and label map
    utils.save_volume(t1_im, brain_generator_gmm_sampling.aff, brain_generator_gmm_sampling.header,
                      os.path.join(result_dir, '%s_%s.nii.gz' % (output_file_name, '0000')))
    utils.save_volume(t2_im, brain_generator_gmm_sampling.aff, brain_generator_gmm_sampling.header,
                      os.path.join(result_dir, '%s_%s.nii.gz' % (output_file_name, '0001')))
    utils.save_volume(lab, brain_generator_gmm_sampling.aff, brain_generator_gmm_sampling.header,
                      os.path.join(result_dir, '%s.nii.gz' % output_file_name))


def create_deformed_labels(labels_dir, result_dir):
    mkdir(result_dir)
    brain_generator = BrainGenerator(labels_dir)
    _, lab = brain_generator.generate_brain()
    output_file_name = 'deformed_labels_1'
    lab_dir = os.path.join(result_dir, "lab")
    mkdir(lab_dir)
    utils.save_volume(
        lab, brain_generator.aff, brain_generator.header, os.path.join(lab_dir, '%s.nii.gz' % output_file_name))


def create_gmm_sampling_image(labels_dir, result_dir, prior_means, prior_stds):
    generation_classes = get_generation_classes()
    generation_labels = get_generation_labels()
    brain_generator = \
        BrainGenerator(
            labels_dir, generation_labels=generation_labels, generation_classes=generation_classes,
            prior_means=prior_means, prior_stds=prior_stds, flipping=False, scaling_bounds=False, rotation_bounds=False,
            shearing_bounds=False,
            bias_field_std=0.0,
            bias_shape_factor=0.0)
    output_file_name = 'gmm_sampling'
    create_images(result_dir, brain_generator, output_file_name)

def create_images(result_dir, brain_generator, output_file_name):
    t1_im, lab = brain_generator.generate_brain()
    t1_im_dir = os.path.join(result_dir, 't1_im')
    mkdir(t1_im_dir)
    utils.save_volume(t1_im, brain_generator.aff, brain_generator.header,
                      os.path.join(t1_im_dir, '%s_%s.nii.gz' % (output_file_name, '0000')))
    lab_im_dir = os.path.join(result_dir, 'lab')
    mkdir(lab_im_dir)
    utils.save_volume(lab, brain_generator.aff, brain_generator.header,
                      os.path.join(lab_im_dir, '%s_%s.nii.gz' % (output_file_name, '1')))

def create_bias_corruption_image(labels_dir, result_dir, prior_means, prior_stds):
    generation_classes = get_generation_classes()
    generation_labels = get_generation_labels()
    brain_generator = \
        BrainGenerator(
            labels_dir, generation_labels=generation_labels, generation_classes=generation_classes,
            prior_means=prior_means, prior_stds=prior_stds, flipping=False, scaling_bounds=False, rotation_bounds=False,
            shearing_bounds=False)
    output_file_name = 'bias_corruption'
    create_images(result_dir, brain_generator, output_file_name)


def create_downsampling_image(labels_dir, result_dir, prior_means, prior_stds):
    generation_classes = get_generation_classes()
    generation_labels = get_generation_labels()
    brain_generator = \
        BrainGenerator(
            labels_dir, generation_labels=generation_labels, generation_classes=generation_classes,
            prior_means=prior_means, prior_stds=prior_stds, flipping=False, scaling_bounds=False, rotation_bounds=False,
            shearing_bounds=False, downsample=True)
    output_file_name = 'downsampling'
    create_images(result_dir, brain_generator, output_file_name)


def create_example(example_num):
    example_dir = '../../data/dcan/figure3/example' + str(example_num)
    dir_a = os.path.join(example_dir, 'a')
    dir_b = os.path.join(example_dir, 'b')
    create_deformed_labels(dir_a, dir_b)
    priors_folder = '/home/feczk001/shared/data/nnUNet/intensity_estimation/Task511/priors/'
    t1_prior_means_file = os.path.join(priors_folder, 't1', 'prior_means.npy')
    t1_prior_means = np.load(t1_prior_means_file)
    t1_prior_stds_file = os.path.join(priors_folder, 't1', 'prior_stds.npy')
    t1_prior_stds = np.load(t1_prior_stds_file)
    labels_dir_b = os.path.join(example_dir, 'b/lab')
    dir_c = os.path.join(example_dir, 'c')
    create_gmm_sampling_image(labels_dir_b, dir_c, t1_prior_means, t1_prior_stds)
    labels_dir_c = os.path.join(dir_c, 'lab')
    dir_d = os.path.join(example_dir, 'd')
    create_bias_corruption_image(labels_dir_c, dir_d, t1_prior_means, t1_prior_stds)
    labels_dir_d = os.path.join(dir_d, 'lab')
    dir_e = os.path.join(example_dir, 'e')
    create_downsampling_image(labels_dir_d, dir_e, t1_prior_means, t1_prior_means)


if __name__ == "__main__":
    create_example(1)
    create_example(2)
