# Functions to extract growth parameters
import pandas as pd
from data import daily_report_data, confirmed, deaths, recovered, time_series_date_list


def make_data_global(country='Global'):
    if country == None or country == 'Global':
        df = pd.DataFrame(
            data={
                'confirmed': [confirmed[date].sum() for date in time_series_date_list],
                'deaths': [deaths[date].sum() for date in time_series_date_list],
                'recovered': [recovered[date].sum() for date in time_series_date_list]
            }, index=time_series_date_list)
    else:
        df = pd.DataFrame(
        data={
            # These dictionaries need to include lists, not pd.Series!
            'recovered': data_by_area(area=country, df=recovered).tolist(),
            'confirmed': data_by_area(area=country, df=confirmed).tolist(),
            'deaths': data_by_area(area=country, df=deaths).tolist()
        }, index=time_series_date_list)
    return df

def data_by_area(area='US', col='Country/Region', df=None):
	from data import time_series_date_list
	data =pd.Series(
		[df.loc[(df[col] == area)][date].sum() for date in time_series_date_list],
		)
	return data

def recent_updates(area='US', timedelta='12 hours', sort='Confirmed', df=None):
    ascending = {
        'Province/State': True
    }
    most_recent = df[df['Country/Region'] == area]['Last Update'].max() - pd.Timedelta(timedelta)
    return df[
        (df['Country/Region'] == area) & (df['Last Update'] >= most_recent)].sort_values(
            sort, ascending=ascending.get(sort, False))

def doubling_time(area='US', df=None):
	pass


def last_update(area='US', column='Country/Region'):
	from data import daily_report_data
	if area == 'Global':
		most_recent = daily_report_data['Last Update'].max().to_pydatetime()
	elif area == 'National':
		most_recent = daily_report_data.groupby('Country/Region')['Last Update'].max()['US'].to_pydatetime()
	else:
		most_recent = daily_report_data.groupby(column)['Last Update'].max()[area].to_pydatetime()
	return most_recent




