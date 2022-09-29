from SynthSeg.estimate_priors import build_intensity_stats
import sys


def estimate_intensities(image_dir, labels_dir, estimation_labels, result_dir):
    """Estimate the hyperparameters governing the GMM prior distributions.  Simple uni-modal case.

    Keyword arguments:
    labels_dir -- path of directory containing corresponding label maps
    estimation_labels -- list of labels from which we want to evaluate the GMM prior distributions
    result_dir -- path of folder where to write estimated priors
    """
    build_intensity_stats(list_image_dir=image_dir,
                          list_labels_dir=labels_dir,
                          estimation_labels=estimation_labels,
                          result_dir=result_dir,
                          rescale=True)


if __name__ == "__main__":
    estimation_labels_file = sys.argv[3]

    file1 = open(estimation_labels_file, 'r')
    lines = file1.readlines()
    labels = []
    for line in lines:
        label = int(line.strip())
        labels.append(label)
    estimate_intensities(sys.argv[1], sys.argv[2], labels, sys.argv[4])
