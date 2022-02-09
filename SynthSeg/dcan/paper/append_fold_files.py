import os
import pandas as pd
from os.path import exists


def append_fold_files(results_dir, measures):
    for measure in measures:
        df = None
        folds = ['fold{}'.format(i) for i in range(10)]
        for fold in folds:
            data_file_path = os.path.join(results_dir, fold, measure, f'{measure}.csv')
            if exists(data_file_path):
                next_df = pd.read_csv(data_file_path)
                if df is not None:
                    df = pd.concat([df, next_df], axis=0, ignore_index=True)
                else:
                    df = next_df
        df.to_csv(os.path.join(results_dir, f'{measure}.csv'), index=False)
