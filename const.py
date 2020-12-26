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

DATE = 'Date'
CASES = 'Cases'
DEATHS = 'Deaths'
NEW_CASES, NEW_DEATHS = [f'New {x.lower()}' for x in (CASES, DEATHS)]
NEW_CASES_AVG, NEW_DEATHS_AVG = [f'{x}, 7-day avg'
                                 for x in (NEW_CASES, NEW_DEATHS)]
CASES_NORM, DEATHS_NORM, NEW_CASES_AVG_NORM, NEW_DEATHS_AVG_NORM = [
    f'{x} per 100k' for x in (CASES, DEATHS, NEW_CASES_AVG, NEW_DEATHS_AVG)
]
