from functions import get_time_series, get_daily_reports, get_date_list, list_of_states
from config import config
import pandas as pd

confirmed, deaths, recovered, time_series_dates = get_time_series(local=config['LOCAL'])
daily_report_data, daily_dates = get_daily_reports(local=config['LOCAL'])

time_series_date_list = get_date_list(time_series_dates)
daily_date_list = get_date_list(daily_dates)

def assign_state(state_value):
    from functions import us_state_abbrev, abbrev_us_state
    if state_value in list(us_state_abbrev.keys()):
        # We have a State Name:
        state = state_value
        county = None
    elif ','in state_value:
        # We have a county, State Pair
        county, state_abbrev = [x.strip() for x in state_value.split(',')]
        state_abbrev = state_abbrev.replace('.','') # Watch out for D.C.!
        state = abbrev_us_state[state_abbrev]
    else:
        # It's a cruise ship!
        state = 'Cruise Ships'
        county = None
    return county, state

def get_states(df):
    df['location'] = pd.DataFrame(df['Province/State'].apply(lambda x: assign_state(x)))
    new_col_list = ['County','State']
    for n,col in enumerate(new_col_list):
        df[col] = df['location'].apply(lambda location: location[n])
    df = df.drop('location',axis=1)
    cols = df.columns.tolist()
    df = df[cols[-2:] + cols[:-2]].copy()
    return df

us_confirmed = confirmed[(confirmed['Country/Region'] == 'US')]
us_confirmed = get_states(us_confirmed)
us_deaths = deaths[(deaths['Country/Region'] == 'US')]
us_deaths = get_states(us_deaths)
us_recovered = recovered[(recovered['Country/Region'] == 'US')]
us_recovered = get_states(us_recovered)

# state_confirmed = us_confirmed[us_confirmed['Province/State'].isin(list_of_states)]
# state_recovered = us_recovered[us_recovered['Province/State'].isin(list_of_states)]
# state_deaths = us_deaths[us_deaths['Province/State'].isin(list_of_states)]

# county_confirmed = us_confirmed[us_confirmed['Province/State'].str.contains(',')]
# county_deaths = us_deaths[us_deaths['Province/State'].str.contains(',')]
# county_recovered = us_recovered[us_recovered['Province/State'].str.contains(',')]

# county_confirmed['County'], county_confirmed['State'] = county_confirmed['Province/State'].str.split(',',1).str
# county_recovered['County'], county_recovered['State'] = county_recovered['Province/State'].str.split(',',1).str
# county_deaths['County'], county_deaths['State'] = county_deaths['Province/State'].str.split(',',1).str

# county_confirmed['County'] = county_confirmed['County'].str.strip()
# county_confirmed['State'] = county_confirmed['State'].str.strip()
# county_deaths['County'] = county_deaths['County'].str.strip()
# county_deaths['State'] = county_deaths['State'].str.strip()
# county_recovered['County'] = county_recovered['County'].str.strip()
# county_recovered['State'] = county_recovered['State'].str.strip()

# # Move the columns to the front:
# cols = county_confirmed.columns.tolist()
# county_confirmed = county_confirmed[cols[-2:] + cols[:-2]]
# cols = county_recovered.columns.tolist()
# county_recovered = county_recovered[cols[-2:] + cols[:-2]]
# cols = county_deaths.columns.tolist()
# county_deaths = county_deaths[cols[-2:] + cols[:-2]]


# Let's create a State abbreviation column for county data