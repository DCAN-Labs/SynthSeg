# Author: Paul Reiners

import os.path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    chirality_corrected_folder = sys.argv[1]
    output_folder = os.path.join(chirality_corrected_folder, 'results_by_age/')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    csv_file = os.path.join(chirality_corrected_folder, 'results/dice/dice.csv')
    dice_data_frame = pd.read_csv(csv_file)
    dice_data_frame['age_in_months'] = dice_data_frame.apply(lambda row: row.subject[0], axis=1)
    for age_in_months in range(9):
        age_df = dice_data_frame[dice_data_frame["age_in_months"] == str(age_in_months)]
        age_df = age_df.drop(['age_in_months'], axis=1)
        sns.catplot(kind="box",
                    data=age_df,
                    height=4,
                    aspect=1.5, orient='h')
        sns.stripplot(data=age_df,
                      alpha=0.3,
                      jitter=0.2,
                      color='k', orient='h')
        fig = plt.gcf()
        plt.ylabel("Region")
        plt.title(f'Dice - {age_in_months}-months-old')
        width = 7.0
        height = 10.0
        fig.set_size_inches(width, height)
        plt.savefig(os.path.join(output_folder, f'dice_{age_in_months}-months-old.png'), dpi=100)
