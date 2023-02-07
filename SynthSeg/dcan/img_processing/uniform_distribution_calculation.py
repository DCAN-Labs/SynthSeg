import os

import numpy as np

# ---------- GMM sampling parameters ----------

# Here we use uniform prior distribution to sample the means/stds of the GMM. Because we don't specify prior_means and
# prior_stds, those priors will have default bounds of [25, 225], and [5, 25]. Those values enable to generate a wide
# range of contrasts (often unrealistic), which will make the segmentation network contrast-agnostic.
import utils
from brain_generator import BrainGenerator
from dcan.segmentation_common import get_generation_labels

prior_distributions = 'uniform'

# We regroup labels with similar tissue types into K "classes", so that intensities of similar regions are sampled
# from the same Gaussian distribution. This is achieved by providing a list indicating the class of each label.
# It should have the same length as generation_labels, and follow the same order. Importantly the class values must be
# between 0 and K-1, where K is the total number of different classes.
#
# Example: (continuing the previous one)  generation_labels = [0, 24, 507, 2, 3, 4, 17, 25, 41, 42, 43, 53, 57]
#                                        generation_classes = [0,  1,   2, 3, 4, 5,  4,  6,  7,  8,  9,  8, 10]
# In this example labels 3 and 17 are in the same *class* 4 (that has nothing to do with *label* 4), and thus will be
# associated to the same Gaussian distribution when sampling the GMM.
generation_classes = '../../data/labels_classes_priors/generation_classes.npy'


# ---------- Spatial augmentation ----------

# We now introduce some parameters concerning the spatial deformation. They enable to set the range of the uniform
# distribution from which the corresponding parameters are selected.
# We note that because the label maps will be resampled with nearest neighbour interpolation, they can look less smooth
# than the original segmentations.

flipping = True  # enable right/left flipping
scaling_bounds = 0.15  # the scaling coefficients will be sampled from U(1-scaling_bounds; 1+scaling_bounds)
rotation_bounds = 15  # the rotation angles will be sampled from U(-rotation_bounds; rotation_bounds)
shearing_bounds = 0.012  # the shearing coefficients will be sampled from U(-shearing_bounds; shearing_bounds)
translation_bounds = False  # no translation is performed, as this is already modelled by the random cropping
nonlin_std = 3.  # this controls the maximum elastic deformation (higher = more deformation)
bias_field_std = 0.5  # his controls the maximum bias field corruption (higher = more bias)


# ---------- Resolution parameters ----------

# This enables us to randomise the resolution of the produces images.
# Although being only one parameter, this is crucial !!
randomise_res = True


# ------------------------------------------------------ Generate ------------------------------------------------------
path_label_map = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task552_uniform_distribution_synthseg/labelsTr/'
generation_labels = get_generation_labels()
output_labels = np.copy(generation_labels)
output_shape = None  # shape of the output images, obtained by randomly cropping the generated images
n_examples = 1
# instantiate BrainGenerator object
brain_generator = BrainGenerator(labels_dir=path_label_map,
                                 generation_labels=generation_labels,
                                 prior_distributions=prior_distributions,
                                 generation_classes=generation_classes,
                                 output_labels=output_labels,
                                 n_channels=2,
                                 output_shape=output_shape,
                                 flipping=flipping,
                                 scaling_bounds=scaling_bounds,
                                 rotation_bounds=rotation_bounds,
                                 shearing_bounds=shearing_bounds,
                                 translation_bounds=translation_bounds,
                                 nonlin_std=nonlin_std,
                                 bias_field_std=bias_field_std,
                                 randomise_res=randomise_res)

for n in range(n_examples):

    # generate new image and corresponding labels
    im, lab = brain_generator.generate_brain()

    # save output image and label map
    utils.save_volume(im, brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 'image_%s.nii.gz' % n))
    utils.save_volume(lab, brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 'labels_%s.nii.gz' % n))
