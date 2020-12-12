import os.path

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

CTP = 'ctp'
JHU = 'jhu'
ALL = 'all'

STATE = 'State'
REGION = 'Region'
COUNTY = 'County'

JHU_STATE_DROP = ['Diamond Princess', 'Grand Princess']

POPULATION = 'Population'

_NORM_SUFFIX = 'per {}'
_AVG_SUFFIX = '{}-day avg'

DATE = 'Date'
CASES = 'Cases'
NEW_CASES = 'New cases'
NEW_CASES_NORM = f'{NEW_CASES} {_NORM_SUFFIX}'
NEW_CASES_AVG = f'{NEW_CASES}, {_AVG_SUFFIX}'
NEW_CASES_AVG_NORM = f'{NEW_CASES_AVG} {_NORM_SUFFIX}'

DEATHS = 'Deaths'
NEW_DEATHS = 'New deaths'
NEW_DEATHS_NORM = f'{NEW_DEATHS} {_NORM_SUFFIX}'
NEW_DEATHS_AVG = f'{NEW_DEATHS}, {_AVG_SUFFIX}'
NEW_DEATHS_AVG_NORM = f'{NEW_DEATHS_AVG} {_NORM_SUFFIX}'
