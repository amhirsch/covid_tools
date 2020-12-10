import pandas as pd
import numpy as np

from covid_tools.const import DATE


def group_calc(df, single_group_func, group_col, sort_col=None):
    """Performs a general function on a dataframe with distinct subsets.

    In a tidy, time series dataframe with multiple groups, say states, age
    groups, etc. there is often a need to perform an operation on each group
    individually. This function takes in a dataframe with distinct groups,
    performs a desired operation on each group, and puts the dataframe back
    together.

    Args:
        df: A tidy pandas dataframe which can be broken into non overlapping
            subgroups.
        single_group_func: A function to be performed on a single group. This
            function must accept two parameters: The first parameter is a
            dataframe where each line belongs to a single group, such as the
            subset containing just entries for California, or just the 18-40
            year old population. The second parameter is the name of the group.
            Following our previous example, this would be "California" or
            "18 to 40".
        group_col: The column in df identifying the subgroups, perhaps "State"
            or "Age Group".
        sort_col: An optional argument identifying the column by which to sort
            the dataframe once the individual groups are combined.
    Returns:
        A copy of the original dataframe where the single_group_func is applied
        to each group. Depending on the function, this may add additional
        columns.
    """

    indiv_groups = []
    for group in df[group_col].unique():
        df_group = df[df[group_col] == group]
        indiv_groups.append(single_group_func(df_group, group))
    sort_list = group_col if sort_col is None else [sort_col, group_col]
    return pd.concat(
        indiv_groups).sort_values(sort_list).reset_index(drop=True).copy()


def fill_missing_date(df, date_col):
    """Identifies and fills missing days with a NA marker."""
    df = df.copy()
    correct_range = pd.date_range(
        df[date_col].min(), df[date_col].max(), name=date_col)
    return df.set_index(date_col).reindex(correct_range).reset_index()


def fill_missing_date_groups(df, date_col, group_col):
    """Fills missing date rows for dataframe with multiple groups."""
    def fill_missing_add_group_col(df, group):
        df = fill_missing_date(df, date_col)
        df[group_col] = group
        return df
    return group_calc(df, fill_missing_add_group_col, group_col, date_col)


def daily_change(df, date_col, dep_var_orig, dep_var_dt):
    """Calculates daily change in the dependent variable. Providing date_col
        ensures that there are no missing dates.
    """
    df = df.copy() if date_col is None else fill_missing_date(df, date_col)
    df[dep_var_dt] = df[dep_var_orig].diff()
    return df


def daily_change_groups(df, date_col, dep_var_orig, dep_var_dt, group_col):
    """Calculates the daily change for multiple groups"""
    return group_calc(
        df,
        lambda x,y: daily_change(x, date_col, dep_var_orig, dep_var_dt),
        group_col, date_col)


def rolling_avg(df, date_col, dep_var_orig, dep_var_rolling_avg, window):
    """Calculates a rolling average with the given window. Providing date_col
        ensures there are no missing dates.
    """
    df = df.copy() if date_col is None else fill_missing_date(df, date_col)
    df[dep_var_rolling_avg] = df[
        dep_var_orig].astype('float64').rolling(window).mean()
    return df


def rolling_avg_groups(df, date_col, dep_var_orig, dep_var_rolling_avg, window,
                       group_col):
    return group_calc(
        df,
        lambda x,y: rolling_avg(x, date_col, dep_var_orig, dep_var_rolling_avg,
                                window),
        group_col, date_col)


def normalize_population(df, dep_var_orig, dep_var_norm, pop_size,
                         norm_size=1e5):
    """Normalize population metric"""
    df = df.copy()
    df[dep_var_norm] = df.apply(
        lambda x: x[dep_var_orig] * norm_size / pop_size,
        axis='columns'
    )
    return df.reset_index(drop=True)


def normalize_population_groups(
        df, dep_var_orig, dep_var_norm, group_col, population_mapper,
        norm_size=1e5, date_col=None):
    population_func = (population_mapper.get
                       if isinstance(population_mapper, dict)
                       else population_mapper)
    return group_calc(
        df,
        lambda x, y: normalize_population(x, dep_var_orig, dep_var_norm,
                                          population_func(y), norm_size),
        group_col, date_col)


def combine_groups(df, date_col, subgroup_col, group_mapper, group_col):
    df = df.copy()
    group_func = (group_mapper.get
                  if isinstance(group_mapper, dict) else group_mapper)
    df[group_col] = df[subgroup_col].apply(group_func)
    df = df[df[group_col].notna()]
    return df.groupby([date_col, group_col]).sum().reset_index()


if __name__ == "__main__":
    from covid_tools.sources.query import load_jhu_us
    from covid_tools.const import STATE, COUNTY, CASES, NEW_CASES
    df = load_jhu_us()
    filter_lower_bound = df[DATE].max() - pd.Timedelta(30, 'days')
    df = df[df[DATE] >= filter_lower_bound].copy()
    df_national = df.groupby(DATE).sum().reset_index().copy()
    df_state = df.groupby([DATE, STATE]).sum().reset_index().copy()
    df_los_angeles = df[df[COUNTY]=='Los Angeles'].copy()

    CA = 'California'
    OR = 'Oregon'
    WA = 'Washington'
    pop_chart = {CA: 39_512_223, OR: 4_217_737, WA: 7_614_893}
    df_west = df[
        df[STATE].isin([CA, OR, WA])].groupby([DATE, STATE]).sum().reset_index()

    df_west_missing = df_west.drop(list(range(75, 84))).copy()

