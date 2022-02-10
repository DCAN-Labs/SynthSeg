import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_violin_plots(results_dir, measures):
    # https://mode.com/blog/violin-plot-examples/
    for measure in measures:
        df = set_up_plot(measure, results_dir)
        sns.violinplot(data=df, orient='h')
        plt.savefig(f'../../../img/paper/violinplot/{measure}.png')


def set_up_plot(measure, results_dir):
    data_file_path = os.path.join(results_dir, f'{measure}.csv')
    df = pd.read_csv(data_file_path)
    df.drop('Unknown', axis=1, inplace=True)
    if measure == 'dice':
        # Remove columns with zeros
        # 0 seems to mean NaN to SynthSeg
        df = df.loc[:, (df != 0).all(axis=0)]
    sns.set(style='whitegrid')
    return df


def create_box_plots(results_dir, measures):
    # https://mode.com/blog/violin-plot-examples/
    for measure in measures:
        df = set_up_plot(measure, results_dir)
        sns.catplot(data=df, orient='h', kind='box')
        plt.savefig(f'../../../img/paper/boxplot/{measure}.png')


def create_cat_plots(results_dir, measures):
    # https://mode.com/blog/violin-plot-examples/
    for measure in measures:
        df = set_up_plot(measure, results_dir)
        sns.catplot(data=df, orient='h')
        plt.savefig(f'../../../img/paper/catplot/{measure}.png')

if __name__ == "__main__":
    results_folder = '/home/miran045/reine097/projects/SynthSeg/data/dcan/paper/measure_tables'
    msrs = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    create_violin_plots(results_folder, msrs)
    create_box_plots(results_folder, msrs)
    create_cat_plots(results_folder, msrs)
