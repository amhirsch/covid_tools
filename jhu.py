import datetime as dt
import json
import requests
import numpy as np

from covid_tools.sources import load_jhu_us_cases, load_jhu_us_deaths, load_jhu_us

JHU_CSSE_NCOV_LIVE_URL = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query'

US_QUERY_PARAMS = {
    'where': "Country_Region='US'",
    'outFields': 'Last_Update,Confirmed,Deaths',
    'f': 'json',
}

def get_jhu_us_aggregate(fetch=False):
    df_jhu = load_jhu_us(fetch).groupby(['date']).sum().reset_index()

    calculations = (
        ('cases', 'newCases', 'newCasesAvg', 'newCasesDelta'),
        ('deaths', 'newDeaths', 'newDeathsAvg', 'newDeathsDelta'),
    )
    for variable, raw_change, average, derivative in calculations:
        df_jhu[raw_change] = df_jhu[variable].diff()
        df_jhu[average] = df_jhu[raw_change].astype('float64').rolling(7).mean()
        df_jhu[derivative] = df_jhu[average].diff()

    return df_jhu


def get_jhu_us_states(fetch=False):
    df = load_jhu_us(fetch)
    df = df.loc[~df.loc[:, 'state'].isin(('Diamond Princess', 'Grand Princess'))]
    df = df.groupby(['date', 'state']).sum().reset_index().convert_dtypes()

    # states = df.loc[:, 'state'].unique()
    # for state in states:
    #     state_mask = df.loc[:, 'state'] = state

    return df


def fetch_us_live_total():
    r = requests.get(JHU_CSSE_NCOV_LIVE_URL, params=US_QUERY_PARAMS)
    if r.status_code == 200:
        response = json.loads(r.text)['features'][0]['attributes']
        response['Last_Update'] = dt.datetime.fromtimestamp(
            response['Last_Update'] // 1e3)
        return response
    raise ConnectionError('ArcGIS API Retruned a Non-200 HTTP Code')


def fetch_us_live_new(fetch=False):
    previous_day_cases = load_jhu_us_cases(fetch, tidy=False).iloc[:,-1].sum()
    previous_day_deaths = load_jhu_us_deaths(fetch, tidy=False).iloc[:,-1].sum()
    current = fetch_us_live_total()
    return {
        'Last Update': current['Last_Update'],
        'New Cases': current['Confirmed'] - previous_day_cases,
        'New Deaths': current['Deaths'] - previous_day_deaths,
    }

def display_us_live(fetch=False):
    live_data = fetch_us_live_new()
    return 'Last Update:\t{}\nNew Cases:\t{}\nNew Deaths:\t{}'.format(
        live_data['Last Update'].strftime('%I:%M %p'),
        live_data['New Cases'], live_data['New Deaths'])
