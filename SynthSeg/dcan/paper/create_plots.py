# Author: Paul Reiners

import os
import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def set_up_plot(measure, results_dir, include_measure_dir=True):
    if include_measure_dir:
        data_file_path = os.path.join(results_dir, measure, f'{measure}.csv')
    else:
        data_file_path = os.path.join(results_dir, f'{measure}.csv')
    df = pd.read_csv(data_file_path)
    df.drop('Unknown', axis=1, inplace=True)
    plt.clf()
    sns.set(style='whitegrid')
    sns.color_palette("colorblind")
    return df


def create_box_plots(results_dir, measures, include_measure_dir=True):
    for measure in measures:
        df = set_up_plot(measure, results_dir, include_measure_dir)
        sns.catplot(data=df, orient='h', kind='box')
        create_figure(results_dir, measure, 'boxplot')


def create_figure(results_dir, measure, folder):
    fig = plt.gcf()
    plt.ylabel("Region")
    plt.title(measure)
    width = 7.0
    if measure == 'dice':
        height = 10.0
    else:
        height = 11.0
    fig.set_size_inches(width, height)
    fig_folder = os.path.join(results_dir, folder)
    if not os.path.exists(fig_folder):
        os.makedirs(fig_folder)
    plt.savefig(os.path.join(fig_folder, f'{measure}.png'), dpi=100)


def create_cat_plots(results_dir, measures, include_measure_dir=True):
    for measure in measures:
        df = set_up_plot(measure, results_dir, include_measure_dir)
        # make boxplot with Catplot
        sns.catplot(kind="box",
                    data=df,
                    height=4,
                    aspect=1.5, orient='h')
        # add data points to boxplot with stripplot
        sns.stripplot(data=df,
                      alpha=0.3,
                      jitter=0.2,
                      color='k', orient='h')
        create_figure(results_dir, measure, 'catplot')


def create_strip_plots(results_dir, measures, include_measure_dir=True):
    for measure in measures:
        df = set_up_plot(measure, results_dir, include_measure_dir)
        sns.stripplot(data=df, orient='h')
        create_figure(results_dir, measure, 'stripplot')


if __name__ == "__main__":
    # Set Matplotlib defaults
    plt.rc('figure', autolayout=True)
    plt.rc('axes', labelweight='bold', labelsize='large',
           titleweight='bold', titlesize=18, titlepad=10)
    plt.rc('image', cmap='magma')

    results_folder = sys.argv[1]
    msrs = ['dice', 'hausdorff', 'hausdorff_95', 'hausdorff_99', 'mean_distance']
    create_cat_plots(results_folder, msrs, include_measure_dir=False)
