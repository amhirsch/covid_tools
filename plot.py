import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from covid_tools.calc import fill_missing_date, fill_missing_date_groups

sns.set()

def ts_plot_setup(dpi=100, x_rotation=60):
    fig, ax = plt.subplots(dpi=dpi)
    ax.tick_params('x', labelrotation=x_rotation)
    return fig, ax

def basic_ts_plot(df, dep_var_col, date_col='date', plot_type='scatter'):
    fig, ax = ts_plot_setup()
    if plot_type == 'scatter':
        ax.scatter(df[date_col], df[dep_var_col].astype('float64'))
    elif plot_type == 'line':
        ax.plot(date_col, dep_var_col, data=df)
    ax.set_xlim(df[date_col].min()-pd.Timedelta(1, 'day'),
                df[date_col].max()+pd.Timedelta(1, 'day'))
    ax.set_ylabel(dep_var_col)
    return fig, ax


def convert_to_np_nan(df):
    return df.copy().replace({pd.NA: np.nan})


def daily_and_avg_static(df, date_col, daily_change_col, rolling_avg_col, ax):
    ax.tick_params('x', labelrotation=90)
    sns.scatterplot(x=date_col, y=daily_change_col, data=df, ax=ax)
    sns.lineplot(x=date_col, y=rolling_avg_col, data=df, ax=ax,
                 label=rolling_avg_col)
    ax.legend()
    return ax


def comparative_static(df, date_col, dep_var_col, group_col, ax):
    ax.tick_params('x', labelrotation=90)
    sns.lineplot(x=date_col, y=dep_var_col, hue=group_col, data=df, ax=ax)
    return ax


def daily_and_avg_interactive(df, date_col, daily_change_col, rolling_avg_col):
    df = convert_to_np_nan(fill_missing_date(df, date_col))
    fig = go.Figure()
    fig.add_scatter(x=df[date_col], y=df[daily_change_col], mode='markers',
                    name=daily_change_col)
    fig.add_scatter(x=df[date_col], y=df[rolling_avg_col], mode='lines',
                    line_color=px.colors.qualitative.Plotly[0],
                    name=rolling_avg_col)
    return fig


def comparative_interactive(df, date_col, dep_var_raw_col, dep_var_norm_col,
                            group_col):
    df = convert_to_np_nan(fill_missing_date_groups(df, date_col, group_col))
    return px.line(df, x=date_col, y=dep_var_norm_col, color=group_col,
                   hover_data=[dep_var_raw_col])
