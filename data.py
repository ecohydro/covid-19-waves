from functions import (
	get_time_series, get_daily_reports, get_date_list, list_of_states,
	make_state_labels, make_country_labels, get_states
	)
from config import config
import pandas as pd

confirmed, deaths, recovered, time_series_dates = get_time_series(local=config['LOCAL'])
daily_report_data, daily_dates = get_daily_reports(local=config['LOCAL'])

daily_report_data = get_states(daily_report_data)
time_series_date_list = get_date_list(time_series_dates)
daily_date_list = daily_dates.tolist()

us_confirmed = confirmed[(confirmed['Country/Region'] == 'US')].copy()
us_confirmed = get_states(us_confirmed)
us_deaths = deaths[(deaths['Country/Region'] == 'US')].copy()
us_deaths = get_states(us_deaths)
us_recovered = recovered[(recovered['Country/Region'] == 'US')].copy()
us_recovered = get_states(us_recovered)

state_labels = make_state_labels(data=us_confirmed)
country_labels = make_country_labels(data=confirmed)
