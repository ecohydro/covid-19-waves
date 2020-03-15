# Functions to extract growth parameters
import pandas as pd

def data_by_area(area='US', col='Country/Region', df=None):
	from data import time_series_date_list
	data =pd.Series(
		[df.loc[(df[col] == area)][date].sum() for date in time_series_date_list],
		)
	return data
