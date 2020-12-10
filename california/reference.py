import pandas as pd

from covid_tools.const import *
import covid_tools.calc

POPULATION_XLSX = 'P1_County_1yr.xlsx'
POPULATION_PICKLE = 'ca_county_population.pickle'
COUNTY = 'County'
POPULATION = 'Population'

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

CA_COUNTY = pd.read_excel(POPULATION_XLSX, header=2, index_col=0, usecols='A,L',
                          nrows=59)
CA_COUNTY.drop('California', inplace=True)
CA_COUNTY.reset_index(inplace=True)
CA_COUNTY.rename(columns={POPULATION: COUNTY, '2020': POPULATION}, inplace=True)
CA_COUNTY[COUNTY] =  CA_COUNTY[COUNTY].apply(lambda x: x[:-7]).convert_dtypes()
CA_COUNTY[REGION] = CA_COUNTY[COUNTY].apply(CA_REGIONS.get).astype('category')
CA_COUNTY.set_index(COUNTY, inplace=True)

CA_REGION_POPULATION = CA_COUNTY.groupby(REGION).sum()


if __name__ == "__main__":
    import covid_tools.calc
    import covid_tools.sources.query