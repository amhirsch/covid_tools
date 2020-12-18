import pandas as pd

from covid_tools.const import *
import covid_tools.calc

POPULATION_CSV = os.path.join(DATA_DIR, 'ca_county_p1a.csv')

NC = 'Northern California'
BA = 'Bay Area'
GS = 'Greater Sacramento'
SJV = 'San Joaquin Valley'
SC = 'Southern California'

CA_REGIONS = {
    'Alameda': BA,
    'Alpine': GS,
    'Amador': GS,
    'Butte': GS,
    'Calaveras': SJV,
    'Colusa': GS,
    'Contra Costa': BA,
    'Del Norte': NC,
    'El Dorado': GS,
    'Fresno': SJV,
    'Glenn': NC,
    'Humboldt': NC,
    'Imperial': SC,
    'Inyo': SC,
    'Kern': SJV,
    'Kings': SJV,
    'Lake': NC,
    'Lassen': NC,
    'Los Angeles': SC,
    'Madera': SJV,
    'Marin': BA,
    'Mariposa': SJV,
    'Mendocino': NC,
    'Merced': SJV,
    'Modoc': NC,
    'Mono': SC,
    'Monterey': BA,
    'Napa': BA,
    'Nevada': GS,
    'Orange': SC,
    'Placer': GS,
    'Plumas': GS,
    'Riverside': SC,
    'Sacramento': GS,
    'San Benito': SJV,
    'San Bernardino': SC,
    'San Diego': SC,
    'San Francisco': BA,
    'San Joaquin': SJV,
    'San Luis Obispo': SC,
    'San Mateo': BA,
    'Santa Barbara': SC,
    'Santa Clara': BA,
    'Santa Cruz': BA,
    'Shasta': NC,
    'Sierra': GS,
    'Siskiyou': NC,
    'Solano': BA,
    'Sonoma': BA,
    'Stanislaus': SJV,
    'Sutter': GS,
    'Tehama': NC,
    'Trinity': NC,
    'Tulare': SJV,
    'Tuolumne': SJV,
    'Ventura': SC,
    'Yolo': GS,
    'Yuba': GS,
}

CA_COUNTIES = pd.read_csv(POPULATION_CSV)
CA_COUNTIES[REGION] = CA_COUNTIES[COUNTY].apply(
    CA_REGIONS.get).astype('category')
CA_COUNTIES.set_index(COUNTY, inplace=True)
CA_COUNTY_POPULATIONS = CA_COUNTIES.loc[:, POPULATION]

CA_REGION_POPULATIONS = CA_COUNTIES.groupby(REGION).sum().loc[:, POPULATION]


if __name__ == "__main__":
    import covid_tools.calc
    import covid_tools.query
