import os
import pandas as pd

time_series_files = [
	'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv',
	'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv',
	'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv',
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'       
]

for file in time_series_files:
	os.system("wget -N --directory-prefix='./data' {file}".format(file=file))

daily_report_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

start_date = pd.to_datetime('01/22/2020')
end_date = pd.to_datetime('today')

dates = pd.date_range(start_date, end_date)

for date in dates:
    # File format: 'MM-DD-YYYY.csv'
    date_str = date.strftime('%m-%d-%Y')
    file_name =date_str + '.csv'
    url = daily_report_url + file_name
    # print(url)
    try:
    	os.system("wget -N --directory-prefix='./data' {file}".format(file=url))
    except:
        print("Failed to save {file}".format(file=file_name))
