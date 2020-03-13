import pandas as pd
import io
import requests
import datetime


def get_date_list(dates):
	return [date.strftime('%-m/%-d/%y') for date in dates]


def get_time_series(local=True):

	ts = {}
	if local == False:
		time_series_files = {
	    	'Confirmed':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv',
	    	'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv',
	    	'Recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
		}
	else:
		time_series_files = {
	    	'Confirmed':'data/time_series_19-covid-Confirmed.csv',
	    	'Deaths': 'data/time_series_19-covid-Deaths.csv',
	    	'Recovered': 'data/time_series_19-covid-Recovered.csv'
		}

	confirmed = pd.read_csv( time_series_files['Confirmed'])
	deaths = pd.read_csv( time_series_files['Deaths'])
	recovered = pd.read_csv( time_series_files['Recovered'])

	return confirmed, deaths, recovered

def get_daily_reports(local=True):

	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	daily_reports = {}
		
	if local == True:
		for date in dates:
			date_str = date.strftime('%m-%d-%Y')
			file_name = 'data/' + date_str + '.csv'
			try:
				daily_reports[date_str] = pd.read_csv(file_name)
			except:
				print("Failed to load {file}".format(file=file_name))
	elif local == False:
		daily_report_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
		for date in dates:
			# File format: 'MM-DD-YYYY.csv'
			date_str = date.strftime('%m-%d-%Y')
			file_name =date_str + '.csv'
			url = daily_report_url + file_name
			try:
				daily_reports[date_str] = pd.read_csv(url)
			except:
				print("Failed to load {file}".format(file=file_name))

	valid_dates = [pd.to_datetime(date) for date in list(daily_reports.keys())]
	return daily_reports, valid_dates
