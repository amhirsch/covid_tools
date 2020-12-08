import pandas as pd
import numpy as np


def fill_missing_date(df, date_col='date'):
    min_date = df.loc[:, date_col].min()
    max_date = df.loc[:, date_col].max()
    correct_range = pd.date_range(min_date, max_date, name=date_col)
    return df.set_index(date_col).reindex(correct_range).reset_index()


def fill_missing_date_multi_groups(df, group_col='group', date_col='date'):
    indiv_groups = []
    for group in df[group_col].unique():
        df_group = df[df[group_col] == group]
        indiv_groups.append(fill_missing_date(df_group))
    return pd.concat(indiv_groups).sort_values([date_col, group_col])


if __name__ == "__main__":
    df_test = pd.DataFrame({
        'date': pd.Series(pd.date_range('2020-12-01', '2020-12-07')),
        'numbers': [1, 2, 3, 4, 5, 6, 7],
        'letters': ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    })

    df_missing = df_test.drop(3).drop(4)

    df_group_a = df_missing.copy()
    df_group_a['group'] = 'A'

    df_group_b = df_missing.copy()
    df_group_b['group'] = 'B'

    df_groups = pd.concat([df_group_a, df_group_b])