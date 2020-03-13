import dash_core_components as dcc
import dash_html_components as html
import dash_table
from components import Header, print_button
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd


from functions import get_time_series, get_daily_reports, get_date_list

confirmed, deaths, recovered = get_time_series(local=True)
daily_report_data, dates = get_daily_reports(local=True)

date_list = get_date_list(dates)

totals_by_day = pd.DataFrame(
    data={
        'confirmed': [confirmed[date].sum() for date in date_list],
        'deaths': [deaths[date].sum() for date in date_list],
        'recovered': [recovered[date].sum() for date in date_list]
    }, index=date_list)


current_day = max(dates).to_pydatetime()
first_day = min(dates).to_pydatetime()


layout_global = html.Div([
	html.Div([
		# Covid Header
		Header(),
		# Date Picker
		html.Div([
			dcc.DatePickerRange(
				id='my-date-picker-range-global',
				min_date_allowed=first_day,
				max_date_allowed=current_day,
				initial_visible_month=dt(current_day.year, current_day.month, 1),
				start_date=(current_day - timedelta(6)),
				end_date=current_day
				),
			html.Div(id='output-container-date-picker-range-global')
			], className="row ", style = {'marginTop': 30, 'marginBottom': 15}),
		# Header Bar
		html.Div([
			html.H6(["Global COVID-19 Cases"], className="gs-header gs-text-header padded", style={'marginTop': 15})
			]),
		# Radio Button
		html.Div([
			dcc.RadioItems(
				options=[
					{'label': 'Condensed Data Table', 'value':'Condensed'},
					{'label': 'Complete Data Table', 'value':'Complete'},
				], value='Condensed',
				labelStyle={
					'display':'inline-block',
					'width':'20%',
					'margin':'auto',
					'marginTop': 15,
					'paddingLeft': 15},
				id='radio-button-global'
			)
			]),
		# First Data Table
		html.Div([
			dash_table.DataTable(
				id='datatable-global',
				columns=[{

				}]
				)
			])

		])
	])


layout_index = html.Div([

	])

layout_us = html.Div([


	])

layout_ca = html.Div([


	])