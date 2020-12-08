import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams.update({'figure.autolayout': True})
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
 