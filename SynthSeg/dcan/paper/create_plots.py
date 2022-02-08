import os

import pandas as pd
import seaborn
import matplotlib.pyplot as plt


def create_plots(results_dir):
    measures = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    for measure in measures:
        data_file_path = os.path.join(results_dir, f'{measure}.csv')
        df = pd.read_csv(data_file_path)
        cols = df.columns.tolist()
        cols = cols[:1] + [str(col) for col in sorted([int(col) for col in cols[1:]])]
        df = df[cols]
        seaborn.set(style='whitegrid')
        seaborn.violinplot(data=df)
        plt.savefig(f'../../../img/paper/{measure}.png')
