import numpy as np


labels = [0]
filename = '../../data/labels_classes_priors/dcan/Freesurfer_LUT_DCAN.md'
with open(filename) as f:
    for index, line in enumerate(f):
        line  = line.strip()
        if len(line) > 0:
            print("Line {}: {}".format(index, line))
            if line[0] != '#':
                parts = line.split()
                label = int(parts[0])
                labels.append(label)
a1D = np.array(labels)
out_file = '/home/feczk001/shared/data/nnUNet/t1_intensity_estimation/generation_labels.npy'
np.save(out_file, a1D)
