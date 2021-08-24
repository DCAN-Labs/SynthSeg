"""
Examples to show how to
We do not provide example images and associated label maps, so do not try to run this directly !
"""
import numpy as np

from SynthSeg.estimate_priors import build_intensity_stats
import sys


def main(image_dir = '/image_folder/t1', labels_dir = '/labels_folder',
         estimation_labels = '../../data/labels_classes_priors/generation_labels.npy',
         result_dir = '../../data/t1_priors'):
    """Estimate the hyperparameters governing the GMM prior distributions.  Simple uni-modal case.

    Keyword arguments:
    image_dir -- path of directory containing the images (default '/image_folder/t1')
    labels_dir -- path of directory containing corresponding label maps (default '/labels_folder')
    estimation_labels -- list of labels from which we want to evaluate the GMM prior distributions (default
                         '../../data/labels_classes_priors/generation_labels.npy')
    result_dir -- path of folder where to write estimated priors (default '../../data/t1_priors')
    """
    build_intensity_stats(list_image_dir=image_dir,
                          list_labels_dir=labels_dir,
                          estimation_labels=estimation_labels,
                          result_dir=result_dir,
                          rescale=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
