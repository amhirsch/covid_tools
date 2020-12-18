import datetime as dt
import json
import locale

import bs4
import requests
import numpy as np

from covid_tools.query import load_jhu_us_cases, load_jhu_us_deaths, load_jhu_us
from covid_tools.const import *

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

JHU_CSSE_NCOV_LIVE_URL = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query'
QUERY_UPDATE = 'Last_Update'
QUERY_CONFIRMED = 'Confirmed'
QUERY_DEATHS = 'Deaths'
LAST_UPDATE = 'Last update'

def US_QUERY_PARAMS():
    return {
        'where': "Country_Region='US'",
        'outFields': ','.join((QUERY_UPDATE, QUERY_CONFIRMED, QUERY_DEATHS)),
        'returnGeometry': 'false',
    }

def get_jhu_us_aggregate(fetch=False):
    df_jhu = load_jhu_us(fetch).groupby([DATE]).sum().reset_index()
    return df_jhu


def get_jhu_us_states(fetch=False):
    df = load_jhu_us(fetch)
    df = df.loc[~df.loc[:, STATE].isin(('Diamond Princess', 'Grand Princess'))]
    df = df.groupby([DATE, STATE]).sum().reset_index().convert_dtypes()
    return df


def fetch_us_live_total(html=False):
    params = US_QUERY_PARAMS()
    params['f'] = 'html' if html else 'json'
    r = requests.get(JHU_CSSE_NCOV_LIVE_URL, params=params)
    if r.status_code == 200:
        if html:
            response = {}
            for row in  (
                bs4.BeautifulSoup(r.text, 'html.parser')
                .find('table', class_='ftrTable')
                .find_all('tr')
            ):
                key, value = [
                    x.get_text(strip=True) for x in row.find_all('td')]
                key = key.rstrip(':')
                response[key] = value
            response[QUERY_UPDATE] = (
                dt.datetime.strptime(response[{LAST_UPDATE}],
                                     '%m/%d/%Y %I:%M:%S %p')
                + (dt.datetime.fromtimestamp(0)
                   - dt.datetime.utcfromtimestamp(0))
            )
            response[QUERY_CONFIRMED] = int(response[QUERY_CONFIRMED])
            response[QUERY_DEATHS] = int(response[QUERY_DEATHS])
            return response
        else:
            response = json.loads(r.text)['features'][0]['attributes']
            response[QUERY_UPDATE] = dt.datetime.fromtimestamp(
                response[QUERY_UPDATE] // 1000)
        return response
    raise ConnectionError('ArcGIS API Retruned a Non-200 HTTP Code')


def fetch_us_live_new(fetch=False, html=False):
    previous_day_cases = load_jhu_us_cases(fetch, tidy=False).iloc[:,-1].sum()
    previous_day_deaths = load_jhu_us_deaths(fetch, tidy=False).iloc[:,-1].sum()
    current = fetch_us_live_total(html)
    return {
        LAST_UPDATE: current[QUERY_UPDATE],
        NEW_CASES: current[QUERY_CONFIRMED] - previous_day_cases,
        NEW_DEATHS: current[QUERY_DEATHS] - previous_day_deaths,
    }


def display_us_live(fetch=False, html=False):
    live_data = fetch_us_live_new(fetch, html)
    return (
        f"{LAST_UPDATE}:\t{live_data[LAST_UPDATE].strftime('%I:%M %p')}\n"
        f"{NEW_CASES}:\t{live_data[NEW_CASES]:,}\n"
        f"{NEW_DEATHS}:\t{live_data[NEW_DEATHS]:,}"
    )
