import pandas as pd
import io
import requests
import datetime

us_state_abbrev = {
	'Alabama': 'AL',
	'Alaska': 'AK',
	'Arizona': 'AZ',
	'Arkansas': 'AR',
	'California': 'CA',
	'Colorado': 'CO',
	'Connecticut': 'CT',
	'Delaware': 'DE',
	'District of Columbia': 'DC',
	'Florida': 'FL',
	'Georgia': 'GA',
	'Hawaii': 'HI',
	'Idaho': 'ID',
	'Illinois': 'IL',
	'Indiana': 'IN',
	'Iowa': 'IA',
	'Kansas': 'KS',
	'Kentucky': 'KY',
	'Louisiana': 'LA',
	'Maine': 'ME',
	'Maryland': 'MD',
	'Massachusetts': 'MA',
	'Michigan': 'MI',
	'Minnesota': 'MN',
	'Mississippi': 'MS',
	'Missouri': 'MO',
	'Montana': 'MT',
	'Nebraska': 'NE',
	'Nevada': 'NV',
	'New Hampshire': 'NH',
	'New Jersey': 'NJ',
	'New Mexico': 'NM',
	'New York': 'NY',
	'North Carolina': 'NC',
	'North Dakota': 'ND',
	'Northern Mariana Islands':'MP',
	'Ohio': 'OH',
	'Oklahoma': 'OK',
	'Oregon': 'OR',
	'Palau': 'PW',
	'Pennsylvania': 'PA',
	'Puerto Rico': 'PR',
	'Rhode Island': 'RI',
	'South Carolina': 'SC',
	'South Dakota': 'SD',
	'Tennessee': 'TN',
	'Texas': 'TX',
	'Utah': 'UT',
	'Vermont': 'VT',
	'Virgin Islands': 'VI',
	'Virginia': 'VA',
	'Washington': 'WA',
	'West Virginia': 'WV',
	'Wisconsin': 'WI',
	'Wyoming': 'WY',
}

# thank you to @kinghelix and @trevormarburger for this idea
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

list_of_states=list(us_state_abbrev.keys()) + ['Diamond Princess','Grand Princess']

def add_new_state_data(us_confirmed, us_deaths, county_data):

	start_date = pd.to_datetime('03/22/2020')
	end_date = pd.to_datetime('today')

	state_data = county_data.groupby(['Date', 'Province_State']).sum().reset_index()

	# Create a new column dictionary
	new_confirmed = {}
	new_deaths = {}
	dates = pd.date_range(start_date, end_date)
	for date in dates:
			date_str = date.strftime('%-m/%-d/%y')
			new_confirmed[date_str] = []
			new_deaths[date_str] = []

	for state in us_confirmed.index:
			new_state_data = state_data[state_data['Province_State'] == state]
			for date in dates:
				date_str = date.strftime('%-m/%-d/%y')
				try:
					a = new_state_data[new_state_data['Date'] == date.strftime('%Y-%m-%d')]['Confirmed'].values[0]
					new_confirmed[date_str] = new_confirmed[date_str] + [a]
				except:
					# print(state)
					new_confirmed[date_str] = new_confirmed[date_str] + [None]

	for date in list(new_confirmed.keys()):
		us_confirmed.loc[:,date] = new_confirmed[date]


	for state in us_confirmed.index:
			new_state_data = state_data[state_data['Province_State'] == state]
			for date in dates:
				date_str = date.strftime('%-m/%-d/%y')
				try:
					a = new_state_data[new_state_data['Date'] == date.strftime('%Y-%m-%d')]['Deaths'].values[0]
					new_deaths[date_str] = new_deaths[date_str] + [a]
				except:
					# print(state)
					new_deaths[date_str] = new_deaths[date_str] + [None]

	for date in list(new_deaths.keys()):
		us_deaths.loc[:,date] = new_deaths[date]
		
	return us_confirmed, us_deaths

def assign_state(state_value):
	from functions import us_state_abbrev, abbrev_us_state
	state_value = str(state_value)
	if state_value in list(us_state_abbrev.keys()):
		# We have a State Name:
		state = state_value
		county = None
	elif ','in state_value:
		# We have a county, State Pair
		county, state_abbrev = [x.strip() for x in state_value.split(',')]
		state_abbrev = state_abbrev.replace('.','') # Watch out for D.C.!
		state = abbrev_us_state.get(state_abbrev, None)
	else:
		# It's a cruise ship!
		state = state_value
		county = None
	return county, state


def assign_state_daily(x):
	if type(x['Province/State']) is str:
			county, state = assign_state(x['Province/State'])
	elif type(x['Province_State']) is str:
		county = x['Admin2']
		state = x['Province_State']
	else:
		county = None
		state = None
	return county, state

def get_states(df):
	df['location'] = pd.DataFrame(df['Province/State'].apply(lambda x: assign_state(x)))
	new_col_list = ['County','State']
	for n,col in enumerate(new_col_list):
		df[col] = df['location'].apply(lambda location: location[n])
	df = df.drop('location',axis=1)
	cols = df.columns.tolist()
	df = df[cols[-2:] + cols[:-2]].copy()
	if 'Province_State' in df.columns:
		df[df['State'] == None]['State'] = df['Province_State']
	return df

def get_states_daily(df):
	df['location'] =df.apply(lambda x: assign_state_daily(x), axis=1)
	new_col_list = ['County','State']
	for n,col in enumerate(new_col_list):
		df[col] = df['location'].apply(lambda location: location[n])
	df = df.drop('location',axis=1)
	cols = df.columns.tolist()
	df = df[cols[-2:] + cols[:-2]].copy()
	return df

def get_date_list(dates):
	return [date.strftime('%-m/%-d/%y') for date in dates]


remote_time_series_files = {
	'Confirmed':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv',
	'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv',
	'Recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv'
}

local_time_series_files = {
			'Confirmed':'data/time_series_19-covid-Confirmed_archived_0325.csv',
			'Deaths': 'data/time_series_19-covid-Deaths_archived_0325.csv',
			'Recovered': 'data/time_series_19-covid-Recovered_archived_0325.csv'
		}

remote_time_series_files_new = {
			'Confirmed': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
			'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
}

local_time_series_files_new = {
			'Confirmed': 'data/time_series_covid19_confirmed_global.csv',
			'Deaths': 'data/time_series_covid19_deaths_global.csv'
}

def get_time_series(local=True):

	ts = {}
	if local == False:
		time_series_files = remote_time_series_files
	else:
		time_series_files = local_time_series_files
	print(time_series_files['Confirmed'])
	confirmed = pd.read_csv( time_series_files['Confirmed'])
	deaths = pd.read_csv( time_series_files['Deaths'])
	recovered = pd.read_csv( time_series_files['Recovered'])

	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	valid_dates = []
	for date in dates:
		if date.strftime('%-m/%-d/%y') in confirmed.columns:
			valid_dates.append(date)

	return confirmed, deaths, recovered, valid_dates


def get_time_series_new(local=True):

	ts = {}
	if local == False:
		time_series_files = remote_time_series_files_new
	else:
		time_series_files = local_time_series_files_new

	confirmed = pd.read_csv( time_series_files['Confirmed'])
	deaths = pd.read_csv( time_series_files['Deaths'])
	# recovered = pd.read_csv( time_series_files['Recovered'])

	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	valid_dates = []
	for date in dates:
		if date.strftime('%-m/%-d/%y') in confirmed.columns:
			valid_dates.append(date)

	return confirmed, deaths, valid_dates


def get_county_reports():
	daily_reports, valid_dates = get_daily_reports(start_date=pd.to_datetime('03/22/2020'))

	county_reports = daily_reports[daily_reports['Country_Region'] == 'US']
	return county_reports, valid_dates



def get_daily_reports(local=True, start_date=pd.to_datetime('01/22/2020')):
	daily_report_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	daily_reports = {}
	all_reports = []
	for date in dates:
			date_str = date.strftime('%m-%d-%Y')
			file_name =date_str + '.csv'
			if local == True:
#				print('Getting {file} using local data'.format(file=file_name))
				f = 'data/' + file_name
			elif local == False:
#				print('Getting daily reports using github (remote) data')
				f = daily_report_url + file_name
			try:
				df = pd.read_csv(f, header=0)
				df['Date'] = date_str
				if date > pd.to_datetime('03/21/2020'): # Handle the new format.
					df['Last Update'] = df['Last_Update']
					print("loaded {f}".format(f=f))
				all_reports.append(df)
			except:
				print("Failed to load {file}".format(file=file_name))
	daily_reports = pd.concat(all_reports, axis=0, ignore_index=True)
	daily_reports.Date = pd.to_datetime(daily_reports['Date'])
	daily_reports['Last Update'] = pd.to_datetime(daily_reports['Last Update'])
	valid_dates = df.Date.unique()
#	valid_dates = [pd.to_datetime(date) for date in list(daily_reports.keys())]
	return daily_reports, valid_dates

def make_country_labels(by_cases=True, data=None):
	if by_cases == False:
		countries = sorted(data['Country/Region'].drop_duplicates())
	elif by_cases == True:
		countries = list(data.groupby('Country/Region').sum().iloc[:,-2].sort_values(ascending=False).index)

	return [{'label': 'Global', 'value': 'Global'}] + [{'label': country, 'value': country} for country in countries]

def make_state_labels(by_cases=True, data=None):
	if by_cases == False:
		states = sorted(data['State'].drop_duplicates())
	elif by_cases == True:
		states = list(data.groupby('State').sum().iloc[:,-2].sort_values(ascending=False).index)
	return [{'label': 'National', 'value': 'National'}] + [{'label': state, 'value': state} for state in states]

