from functions import (
	get_time_series, get_time_series_new, get_daily_reports, get_date_list, list_of_states,
	make_state_labels, make_country_labels, get_states, get_county_reports, get_states_daily
	)
from config import config
import pandas as pd
import numpy as np
import datetime

confirmed, deaths, time_series_dates = get_time_series_new(local=config['LOCAL'])
daily_report_data, daily_dates = get_daily_reports(local=config['LOCAL'])

county_data, county_dates = get_county_reports()


daily_report_data = get_states_daily(daily_report_data)
time_series_date_list = get_date_list(time_series_dates)
daily_date_list = daily_dates.tolist()

from model import doubling_time, growth_rate

confirmed_totals = confirmed.groupby('Country/Region').sum()
death_totals = deaths.groupby('Country/Region').sum()
# recovered_totals = recovered.groupby('Country/Region').sum()

new_confirmed = confirmed_totals[confirmed_totals.columns[2:]].diff(axis=1)
# new_recovered = recovered_totals[recovered_totals.columns[2:]].diff(axis=1)
new_deaths = death_totals[death_totals.columns[2:]].diff(axis=1)

case_mortality = death_totals/confirmed_totals
# case_recovery = recovered_totals/confirmed_totals

countries = confirmed_totals.index

case_rate = growth_rate(df=confirmed_totals)
death_rate = growth_rate(df=death_totals)

case_doubling = doubling_time(case_rate)
death_doubling = doubling_time(death_rate)

data = []
for country in countries:
    for date in time_series_date_list:
        data.extend(
            [dict(
                country=country,
                state='Nation',
                date=date,
                variable='confirmed',
                value=confirmed_totals.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='deaths',
                value=death_totals.loc[country, date]
            ),
            # dict(
            #     country=country,
            #     state='Nation',
            #     date=date,
            #     variable='recovered',
            #     value=recovered_totals.loc[country, date]
            # ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='new_confirmed',
                value=new_confirmed.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='new_deaths',
                value=new_deaths.loc[country, date]
            ),
            # dict(
            #     country=country,
            #     state='Nation',
            #     date=date,
            #     variable='new_recovered',
            #     value=new_recovered.loc[country, date]
            # ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='case_rate',
                value=case_rate.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='death_rate',
                value=death_rate.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='case_mortality',
                value=case_mortality.loc[country, date]
            ),
            # dict(
            #     country=country,
            #     state='Nation',
            #     date=date,
            #     variable='case_recovery',
            #     value=case_recovery.loc[country, date]
            # ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='case_doubling',
                value=case_doubling.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='death_doubling',
                value=death_doubling.loc[country, date]
            )
            ])

data_df = pd.DataFrame.from_dict(data)


label_dict = dict(
    confirmed='Total Confirmed Cases',
    deaths='Total Deaths',
    # recovered='Total Recovered Cases',
    new_confirmed='New Confirmed Cases',
    new_deaths='New Deaths',
    # new_recovered='New Recovered Cases',
    case_rate='Percent Increase in Confirmed Cases',
    death_rate='Percent Increase in Deaths',
    case_mortality='Cumulative Case Mortality Rate',
    # case_recovery='Cumulative Case Recovery Rate',
    case_doubling='Doubling Time for Confirmed Cases',
    death_doubling='Doubling Time of Deaths'
)

variable_dict = {}
for variable, label in label_dict.items():
	variable_dict[label] = variable

dates = np.array(
	[datetime.datetime.strptime(date, '%m/%d/%y') for date in data_df.date.unique()])
date_strings = [date.strftime('%-m/%-d/%y') for date in dates]


old_confirmed, old_deaths, old_recovered, time_series_dates = get_time_series(local=config['LOCAL'])

us_confirmed = old_confirmed[(old_confirmed['Country/Region'] == 'US')].copy()
us_confirmed = get_states(us_confirmed)

us_confirmed = us_confirmed.groupby('State').sum()

us_deaths = old_deaths[(old_deaths['Country/Region'] == 'US')].copy()
us_deaths = get_states(us_deaths)

us_deaths = us_deaths.groupby('State').sum()


from functions import add_new_state_data

us_confirmed, us_deaths = add_new_state_data(us_confirmed, us_deaths, county_data)

state_labels = make_state_labels(data=us_confirmed)
country_labels = make_country_labels(data=confirmed)



def data_by_area(area='US', col='Country/Region', df=None):
	data =pd.Series(
		[df.loc[(df[col] == area)][date].sum() for date in time_series_date_list],
		)
	return data

def make_data_global(country='Global'):
    if country == None or country == 'Global':
        df = pd.DataFrame(
            data={
                'confirmed': [confirmed[date].sum() for date in time_series_date_list],
                'deaths': [deaths[date].sum() for date in time_series_date_list],
                # 'recovered': [recovered[date].sum() for date in time_series_date_list]
            }, index=time_series_date_list)
    else:
        df = pd.DataFrame(
        data={
            # These dictionaries need to include lists, not pd.Series!
            # 'recovered': data_by_area(area=country, df=recovered).tolist(),
            'confirmed': data_by_area(area=country, df=confirmed).tolist(),
            'deaths': data_by_area(area=country, df=deaths).tolist()
        }, index=time_series_date_list)
    return df

def make_data_state(state='National', limit=28):
    if state == None or state == 'National':
        df = pd.DataFrame(
            data={
                'confirmed': [us_confirmed[date].sum() for date in time_series_date_list],
                'deaths': [us_deaths[date].sum() for date in time_series_date_list],
                # 'recovered': [us_recovered[date].sum() for date in time_series_date_list]
            }, index=time_series_date_list)
    else:
        df = pd.DataFrame(
            data={
            # 'recovered': data_by_area(area=state, df=us_recovered, col='State').tolist(),
            'confirmed': [us_confirmed[us_confirmed.index == state][date].values[0] for date in time_series_date_list],
            'deaths': [us_deaths[us_deaths.index == state][date].values[0] for date in time_series_date_list]
        }, index=time_series_date_list)
    return df.iloc[limit:,:]

