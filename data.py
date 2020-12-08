import pandas as pd

WEEKDAY_MAP = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

def make_region(df, names, populations, date_col, name_col,
                case_col, rate_multiplier=1e5):
    """ Groups areas together to make custom region """
    pass

def new_cases_weekday_breakdown(
        df, new_cases_col, weeks_back=4, date_col='date'):
    df = df[df[date_col]>(df[date_col].max()-pd.Timedelta(7*weeks_back, 'days'))].copy()
    df['dayOfWeek'] = df[date_col].apply(lambda x: x.weekday())
    monthly_cases = df[new_cases_col].sum()
    df_dist = df.groupby('dayOfWeek').sum()
    df_dist.rename(index=WEEKDAY_MAP, inplace=True)
    df_dist['propCases'] = df_dist[
        new_cases_col].apply(lambda x: round(x/monthly_cases*100,2))
    return df_dist.loc[:, ['propCases']]

def weekday_ratio_over_average(
    df, numerator_col, denominator_col, date_col='date', weights=(25, 25, 25, 25)):
    df = df.loc[:, [date_col, numerator_col, denominator_col]].copy()
    df.sort_values(date_col, inplace=True)
    df['dayOfWeek'] = df[date_col].apply(lambda x: x.weekday())
    df['dailyRatio'] = df[numerator_col] / df[denominator_col]
    
    weekday_ratio = {}
    weights_sum = sum(weights)
    weights_normalized = [x/weights_sum for x in weights]
    for i in WEEKDAY_MAP:
        weekday_series = df.loc[df['dayOfWeek']==i, 'dailyRatio']
        weekday_series = weekday_series.iloc[::-1]
        ratio_dot_product = [
            weekday_series.iloc[x]*weights_normalized[x]
            for x in range(len(weights_normalized))]
        weekday_ratio[WEEKDAY_MAP[i]] = round(sum(ratio_dot_product), 4)
    return weekday_ratio
