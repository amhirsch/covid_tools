import pandas as pd

from covid_tools.const import STATE, POPULATION, JHU_STATE_DROP
from covid_tools.sources.query import load_jhu_us_deaths

STATE_POPULATIONS = load_jhu_us_deaths(
    tidy=False).rename(columns={'Province_State': STATE})
STATE_POPULATIONS = (
    STATE_POPULATIONS.loc[:, [STATE, POPULATION]].dropna().groupby(STATE).sum()
    .drop(JHU_STATE_DROP))
