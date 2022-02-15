import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def set_up_plot(measure, results_dir):
    data_file_path = os.path.join(results_dir, f'{measure}.csv')
    df = pd.read_csv(data_file_path)
    df.drop('Unknown', axis=1, inplace=True)
    sns.set(style='whitegrid')
    return df


def create_box_plots(results_dir, measures):
    for measure in measures:
        df = set_up_plot(measure, results_dir)
        sns.catplot(data=df, orient='h', kind='box')
        create_figure(measure, 'boxplot')


def create_figure(measure, folder):
    fig = plt.gcf()
    plt.ylabel("Region")
    plt.title(measure)
    width = 7.0
    if measure == 'dice':
        height = 10.0
    else:
        height = 11.0
    fig.set_size_inches(width, height)
    plt.savefig(f'../../../img/paper/{folder}/{measure}.png', dpi=100)


def create_cat_plots(results_dir, measures):
    for measure in measures:
        df = set_up_plot(measure, results_dir)
        sns.catplot(data=df, orient='h')
        create_figure(measure, 'catplot')

if __name__ == "__main__":
    # Set Matplotlib defaults
    plt.rc('figure', autolayout=True)
    plt.rc('axes', labelweight='bold', labelsize='large',
           titleweight='bold', titlesize=18, titlepad=10)
    plt.rc('image', cmap='magma')

    results_folder = '/home/miran045/reine097/projects/SynthSeg/data/dcan/paper/measure_tables'
    msrs = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    create_box_plots(results_folder, msrs)
    create_cat_plots(results_folder, msrs)
