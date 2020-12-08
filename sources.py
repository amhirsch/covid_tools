import os.path

import pandas as pd
import requests

SOURCES_DIR = os.path.join(os.path.dirname(__file__), 'data')

CTP_US_URL = 'https://api.covidtracking.com/v1/us/daily.csv'
CTP_US_CSV = os.path.join(SOURCES_DIR, 'ctp-us.csv')

JHU_TS_BASE_URL = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/'
JHU_US_CASES_URL = JHU_TS_BASE_URL + 'time_series_covid19_confirmed_US.csv'
JHU_US_DEATHS_URL = JHU_TS_BASE_URL + 'time_series_covid19_deaths_US.csv'
JHU_US_CASES_CSV = os.path.join(SOURCES_DIR, 'jhu-us-cases.csv')
JHU_US_DEATHS_CSV = os.path.join(SOURCES_DIR, 'jhu-us-deaths.csv')


def fetch_source(url, csv):
    r = requests.get(url)
    if r.status_code == 200:
        with open(csv, 'w') as f:
            f.write(r.text)
    else:
        raise ConnectionError('Non 200 HTTP Status Code')


def load_source(url, csv, fetch):
    if not os.path.isfile(csv) or fetch:
        fetch_source(url, csv)
    return pd.read_csv(csv)


def load_ctp_us(fetch=False):
    df = load_source(CTP_US_URL, CTP_US_CSV, fetch)
    df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'].apply(lambda x: str(x)))
    df.drop(columns=['dateChecked','lastModified','hash'], inplace=True)
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def tidy_jhu(df, value_col):
    df.drop(columns=[
        'UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Country_Region',
        'Lat', 'Long_', 'Combined_Key'], inplace=True)
    df.rename(columns={'Admin2': 'county', 'Province_State': 'state'}, inplace=True)
    df = df.melt(('county', 'state'), var_name='date', value_name=value_col)
    df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'])
    df = df.convert_dtypes()
    # df = df.sort_values(['date', 'state', 'county'])
    return df #.reset_index(drop=True)


def load_jhu_us_cases(fetch=False, tidy=True):
    df = load_source(JHU_US_CASES_URL, JHU_US_CASES_CSV, fetch)
    return tidy_jhu(df, 'cases') if tidy else df


def load_jhu_us_deaths(fetch=False, tidy=True):
    df = load_source(JHU_US_DEATHS_URL, JHU_US_DEATHS_CSV, fetch)
    return tidy_jhu(df.drop(columns='Population'), 'deaths') if tidy else df


def load_jhu_us(fetch=False):
    return pd.merge(load_jhu_us_cases(fetch), load_jhu_us_deaths(fetch),
                    on=['date', 'state', 'county'])


def fetch_all():
    load_ctp_us(True)
    load_jhu_us(True)


# def fetch_national():
#     r = requests.get(NATIONAL_DAILY_URL)
#     if r.status_code == 200:
#         with open(NATIONAL_DAILY_CSV, 'w') as f:
#             f.write(r.text)


# def load_national(fetch=False):
#     if not os.path.isfile(NATIONAL_DAILY_CSV) or fetch:
#         fetch_national()
#     df = pd.read_csv(NATIONAL_DAILY_CSV)
#     df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'].apply(lambda x: str(x)))
#     df = df.sort_values('date').reset_index(drop=True)
#     return df
