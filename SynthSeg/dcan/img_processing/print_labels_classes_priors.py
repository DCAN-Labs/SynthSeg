from pathlib import Path
import numpy as np

for path in Path('./data/labels_classes_priors/dcan').rglob('*.npy'):
    p = path.resolve()
    print(p)
    numbers = np.load(p)
    print(numbers)
    print()
    