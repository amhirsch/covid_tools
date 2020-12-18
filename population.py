from covid_tools.const import STATE, POPULATION, JHU_STATE_DROP
from covid_tools.query import load_jhu_us_deaths


STATE_POPULATIONS = (
    load_jhu_us_deaths(tidy=False).rename(columns={'Province_State': STATE})
    .loc[:, [STATE, POPULATION]].dropna().groupby(STATE).sum()
    .drop(JHU_STATE_DROP).loc[:, POPULATION]
)
US_POPULATION = STATE_POPULATIONS.sum()