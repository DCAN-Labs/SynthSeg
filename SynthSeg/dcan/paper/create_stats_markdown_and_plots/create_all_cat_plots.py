import os.path
from pathlib import Path

from dcan.paper.create_only_cat_plots import create_all_cat_plots
src_dir = '/home/feczk001/shared/data/nnUNet/528/'

for i in range(9):
    gt_folder = os.path.join(src_dir, 'labelsTs', f'{i}mo')
    inferred_dir = os.path.join(src_dir, 'infer', f'{i}mo')
    results_folder = os.path.join(src_dir, 'results', f'{i}mo')
    Path(results_folder).mkdir(parents=True, exist_ok=True)
    create_all_cat_plots(gt_folder, inferred_dir, results_folder)
