import os.path
import numpy as np

results_dir = '/home/feczk001/shared/data/nnUNet/segmentations/inferred/PaperCrossValidation/results/fold0/'
dice_file = os.path.join(results_dir, 'dice/dice.npy')
dice = np.load(dice_file)

labels_file = open(os.path.join(results_dir, 'labels.txt'), 'r')
labels_content = labels_file.read()
labels = labels_content.split()
labels = [int(label) for label in labels]
labels_file.close()

path_segs_file = open(os.path.join(results_dir, 'path_segs.txt'), "r")
path_segs_content = path_segs_file.read()
path_segs_content_list = path_segs_content.split()
path_segs_file.close()
