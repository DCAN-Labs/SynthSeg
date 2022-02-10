import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_violin_plots(results_dir, measures):
    # https://mode.com/blog/violin-plot-examples/
    for measure in measures:
        data_file_path = os.path.join(results_dir, f'{measure}.csv')
        df = pd.read_csv(data_file_path)
        sns.set(style='whitegrid')
        sns.violinplot(data=df, orient='h')
        plt.savefig(f'../../../img/paper/{measure}.png')
