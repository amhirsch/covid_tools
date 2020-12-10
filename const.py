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

DATE = 'date'
CASES = 'cases'
NEW_CASES = 'newCases'
DEATHS = 'deaths'
NEW_DEATHS = 'newDeaths'
