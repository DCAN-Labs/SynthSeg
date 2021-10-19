import os

import numpy as np

from SynthSeg import utils
from SynthSeg.brain_generator import BrainGenerator


def generate_overview_diagram(path_label_map, priors_folder, result_dir):
    # general parameters
    output_shape = None  # shape of the output images, obtained by randomly cropping the generated images

    # specify structures from which we want to generate
    # Here we specify the structures in the label maps for which we want to generate intensities.
    # This is given as a list of label values, which do not necessarily need to be present in every label map.
    # However, these labels must follow a specific order: first the non-sided labels, then all the left labels, and
    # finally the corresponding right labels in the same order as the left ones.
    generation_labels = np.array(
        [0,  # background
         24,  # CSF
         14,  # 3rd-Ventricle
         15,  # 4th-Ventricle
         16,  # Brain-Stem
         77,  # WM-hypointensities
         85,  # Optic-Chiasm
         172,  # Vermis
         1,  # Left-Cerebral-Exterior
         2,  # Left-Cerebral-White-Matter
         3,  # Left-Cerebral-Cortex
         4,  # Left-Lateral-Ventricle
         5,  # Left-Inf-Lat-Vent
         6,  # Left-Cerebellum-Exterior
         7,  # Left-Cerebellum-White-Matter
         8,  # Left-Cerebellum-Cortex
         10,  # Left-Thalamus-Proper
         11,  # Left-Caudate
         12,  # Left-Putamen
         13,  # Left-Pallidum
         17,  # Left-Hippocampus
         18,  # Left-Amygdala
         26,  # Left-Accumbens-area
         28,  # Left-VentralDC
         30,  # Left-vessel
         31,  # Left-choroid-plexus
         40,  # Right-Cerebral-Exterior
         41,  # Right-Cerebral-White-Matter
         42,  # Right-Cerebral-Cortex
         43,  # Right-Lateral-Ventricle
         44,  # Right-Inf-Lat-Vent
         45,  # Right-Cerebellum-Exterior
         46,  # Right-Cerebellum-White-Matter
         47,  # Right-Cerebellum-Cortex
         49,  # Right-Thalamus-Proper
         50,  # Right-Caudate
         51,  # Right-Putamen
         52,  # Right-Pallidum
         53,  # right hippocampus
         54,  # Right-Amygdala
         58,  # Right-Accumbens-area
         60,  # Right-VentralDC
         62,  # Right-vessel
         63])  # Right-choroid-plexus

    # specify structures that we want to keep in the output label maps
    output_labels = np.copy(generation_labels)

    # we regroup structures into K classes, so that they share the same distribution for image generation
    # We regroup labels with similar tissue types into K "classes", so that intensities of similar regions are sampled
    # from the same Gaussian distribution. This is achieved by providing a list indicating the class of each label.
    # It should have the same length as generation_labels, and follow the same order. Importantly the class values must
    # be between 0 and K-1, where K is the total number of different classes.
    #
    # Example: (continuing the previous one)  generation_labels = [0, 24, 507, 2, 3, 4, 17, 25, 41, 42, 43, 53, 57]
    #                                        generation_classes = [0,  1,   2, 3, 4, 5,  4,  6,  7,  8,  9,  8, 10]
    # In this example labels 3 and 17 are in the same *class* 4 (that has nothing to do with *label* 4), and thus will
    # be associated to the same Gaussian distribution when sampling the GMM.
    generation_classes = np.array(
        [0,  # background
         1,  # CSF
         2,  # 3rd-Ventricle
         3,  # 4th-Ventricle
         4,  # Brain-Stem
         5,  # WM-hypointensities
         6,  # Optic-Chiasm
         7,  # Vermis
         8,  # Left-Cerebral-Exterior
         9,  # Left-Cerebral-White-Matter
         10,  # Left-Cerebral-Cortex
         11,  # Left-Lateral-Ventricle
         12,  # Left-Inf-Lat-Vent
         13,  # Left-Cerebellum-Exterior
         14,  # Left-Cerebellum-White-Matter
         15,  # Left-Cerebellum-Cortex
         16,  # Left-Thalamus-Proper
         17,  # Left-Caudate
         18,  # Left-Putamen
         19,  # Left-Pallidum
         20,  # Left-Hippocampus
         21,  # Left-Amygdala
         22,  # Left-Accumbens-area
         23,  # Left-VentralDC
         24,  # Left-vessel
         25,  # Left-choroid-plexus
         8,  # Right-Cerebral-Exterior
         9,  # Right-Cerebral-White-Matter
         10,  # Right-Cerebral-Cortex
         11,  # Right-Lateral-Ventricle
         12,  # Right-Inf-Lat-Vent
         13,  # Right-Cerebellum-Exterior
         14,  # Right-Cerebellum-White-Matter
         15,  # Right-Cerebellum-Cortex
         16,  # Right-Thalamus-Proper
         17,  # Right-Caudate
         18,  # Right-Putamen
         19,  # Right-Pallidum
         20,  # right hippocampus
         21,  # Right-Amygdala
         22,  # Right-Accumbens-area
         23,  # Right-VentralDC
         24,  # Right-vessel
         25])  # Right-choroid-plexus

    # We specify here that we type of prior distributions to sample the GMM parameters.
    # By default prior_distribution is set to 'uniform', and in this example we want to change it to 'normal'.
    prior_distribution = 'normal'

    # We specify here the hyperparameters of the prior distributions to sample the means of the GMM.
    # As these prior distributions are Gaussians, they are each controlled by a mean and a standard deviation.
    # Therefore, the numpy array pointed by prior_means is of size (2, K), where K is the nummber of classes specified
    # in generation_classes. The first row of prior_means correspond to the means of the Gaussian priors, and the second
    # row correspond to standard deviations.
    t1_prior_means_file = os.path.join(priors_folder, 't1', 'prior_means.npy')
    t1_prior_means = np.load(t1_prior_means_file)
    t2_prior_means_file = os.path.join(priors_folder, 't2', 'prior_means.npy')
    t2_prior_means = np.load(t2_prior_means_file)
    prior_means = np.concatenate((t1_prior_means, t2_prior_means))
    # same as for prior_means, but for the standard deviations of the GMM.
    t1_prior_stds_file = os.path.join(priors_folder, 't1', 'prior_stds.npy')
    t1_prior_stds = np.load(t1_prior_stds_file)
    t2_prior_stds_file = os.path.join(priors_folder, 't2', 'prior_stds.npy')
    t2_prior_stds = np.load(t2_prior_stds_file)
    prior_stds = np.concatenate((t1_prior_stds, t2_prior_stds))

    ########################################################################################################

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
    brain_generator = BrainGenerator(labels_dir)
    _, lab = brain_generator.generate_brain()
    output_file_name = 'deformed_labels_1'
    utils.save_volume(lab, brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, '%s.nii.gz' % output_file_name))


def create_gmm_sampling_image(labels_dir, result_dir, prior_means, prior_stds):
    generation_classes = np.array(
        [0,  # background
         1,  # CSF
         2,  # 3rd-Ventricle
         3,  # 4th-Ventricle
         4,  # Brain-Stem
         5,  # WM-hypointensities
         6,  # Optic-Chiasm
         7,  # Vermis
         8,  # Left-Cerebral-Exterior
         9,  # Left-Cerebral-White-Matter
         10,  # Left-Cerebral-Cortex
         11,  # Left-Lateral-Ventricle
         12,  # Left-Inf-Lat-Vent
         13,  # Left-Cerebellum-Exterior
         14,  # Left-Cerebellum-White-Matter
         15,  # Left-Cerebellum-Cortex
         16,  # Left-Thalamus-Proper
         17,  # Left-Caudate
         18,  # Left-Putamen
         19,  # Left-Pallidum
         20,  # Left-Hippocampus
         21,  # Left-Amygdala
         22,  # Left-Accumbens-area
         23,  # Left-VentralDC
         24,  # Left-vessel
         25,  # Left-choroid-plexus
         8,  # Right-Cerebral-Exterior
         9,  # Right-Cerebral-White-Matter
         10,  # Right-Cerebral-Cortex
         11,  # Right-Lateral-Ventricle
         12,  # Right-Inf-Lat-Vent
         13,  # Right-Cerebellum-Exterior
         14,  # Right-Cerebellum-White-Matter
         15,  # Right-Cerebellum-Cortex
         16,  # Right-Thalamus-Proper
         17,  # Right-Caudate
         18,  # Right-Putamen
         19,  # Right-Pallidum
         20,  # right hippocampus
         21,  # Right-Amygdala
         22,  # Right-Accumbens-area
         23,  # Right-VentralDC
         24,  # Right-vessel
         25])  # Right-choroid-plexus
    generation_labels = np.array(
        [0,  # background
         24,  # CSF
         14,  # 3rd-Ventricle
         15,  # 4th-Ventricle
         16,  # Brain-Stem
         77,  # WM-hypointensities
         85,  # Optic-Chiasm
         172,  # Vermis
         1,  # Left-Cerebral-Exterior
         2,  # Left-Cerebral-White-Matter
         3,  # Left-Cerebral-Cortex
         4,  # Left-Lateral-Ventricle
         5,  # Left-Inf-Lat-Vent
         6,  # Left-Cerebellum-Exterior
         7,  # Left-Cerebellum-White-Matter
         8,  # Left-Cerebellum-Cortex
         10,  # Left-Thalamus-Proper
         11,  # Left-Caudate
         12,  # Left-Putamen
         13,  # Left-Pallidum
         17,  # Left-Hippocampus
         18,  # Left-Amygdala
         26,  # Left-Accumbens-area
         28,  # Left-VentralDC
         30,  # Left-vessel
         31,  # Left-choroid-plexus
         40,  # Right-Cerebral-Exterior
         41,  # Right-Cerebral-White-Matter
         42,  # Right-Cerebral-Cortex
         43,  # Right-Lateral-Ventricle
         44,  # Right-Inf-Lat-Vent
         45,  # Right-Cerebellum-Exterior
         46,  # Right-Cerebellum-White-Matter
         47,  # Right-Cerebellum-Cortex
         49,  # Right-Thalamus-Proper
         50,  # Right-Caudate
         51,  # Right-Putamen
         52,  # Right-Pallidum
         53,  # right hippocampus
         54,  # Right-Amygdala
         58,  # Right-Accumbens-area
         60,  # Right-VentralDC
         62,  # Right-vessel
         63])  # Right-choroid-plexus
    brain_generator = \
        BrainGenerator(
            labels_dir, generation_labels=generation_labels, generation_classes=generation_classes,
            prior_means=prior_means, prior_stds=prior_stds, flipping=False, scaling_bounds=False, rotation_bounds=False,
            shearing_bounds=False,
                 bias_field_std=0.0,
                 bias_shape_factor=0.0)
    t1_im, _ = brain_generator.generate_brain()
    output_file_name = 'gmm_sampling_1'
    utils.save_volume(t1_im, brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, '%s_%s.nii.gz' % (output_file_name, '0000')))


if __name__ == "__main__":
    labels_dir_1 = '/home/miran045/reine097/projects/SynthSeg/data/dcan/figure3/example1/input'
    results_dir_1 = '/home/miran045/reine097/projects/SynthSeg/data/dcan/figure3/example1/output'
    create_deformed_labels(labels_dir_1, results_dir_1)
    priors_folder = '/home/feczk001/shared/data/nnUNet/intensity_estimation/Task511/priors/'
    t1_prior_means_file = os.path.join(priors_folder, 't1', 'prior_means.npy')
    t1_prior_means = np.load(t1_prior_means_file)
    t1_prior_stds_file = os.path.join(priors_folder, 't1', 'prior_stds.npy')
    t1_prior_stds = np.load(t1_prior_stds_file)
    create_gmm_sampling_image(results_dir_1, results_dir_1, t1_prior_means, t1_prior_stds)
