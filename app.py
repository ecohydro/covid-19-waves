# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

# Read Config Settings from .env file:
from dotenv import load_dotenv
load_dotenv()
config = {}
config['LOCAL'] = str2bool(os.getenv('LOCAL'))
config['DEBUG'] = str2bool(os.getenv('DEBUG'))

from functions import get_time_series, get_daily_reports, get_date_list

confirmed, deaths, recovered, time_series_dates = get_time_series(local=config['LOCAL'])
daily_report_data, daily_dates = get_daily_reports(local=config['LOCAL'])

time_series_date_list = get_date_list(time_series_dates)
daily_date_list = get_date_list(daily_dates)

githublink = 'https://github.com/ecohydro/covid-19-waves'
sourceurl = 'https://github.com/CSSEGISandData/COVID-19'


external_stylesheets = [
	"https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
	"https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
	"//fonts.googleapis.com/css?family=Raleway:400,300,600",
	"https://codepen.io/bcd/pen/KQrXdb.css",
	"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
	"https://codepen.io/dmcomfort/pen/JzdzEZ.css"
]

external_scripts = [
	"https://code.jquery.com/jquery-3.2.1.min.js",
	"https://codepen.io/bcd/pen/YaXojL.js"
]



app = dash.Dash(
	__name__,
	external_scripts=external_scripts,
	external_stylesheets=external_stylesheets,
	url_base_pathname='/covid-19/')

server = app.server
app.config.suppress_callback_exceptions = True


def make_country_labels(by_cases=False):
    
    if by_cases == False:
        countries = sorted(confirmed['Country/Region'].drop_duplicates())
    elif by_cases == True:
        countries = list(confirmed.groupby('Country/Region').sum().iloc[:,-1].sort_values(ascending=False).index)

    return [{'label': 'Global', 'value': 'Global'}] + [{'label': country, 'value': country} for country in countries]

app.layout = html.Div([
    html.H1(children='COVID-19 Dashboard'),

    html.Div(children='''
        Data from Johns Hopkins.
    '''),
    dcc.Dropdown(
        id='global-dropdown',
        options=make_country_labels(by_cases=True),
        value='Global'
        ),
    dcc.Graph(id='global-graph'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
])

# @app.callback(Output('global-graph', 'options'), [Input()])

@app.callback(Output('global-graph', 'figure'), [Input('global-dropdown', 'value')])
def update_global_graph(selected_dropdown_value):
    country = selected_dropdown_value
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
            'recovered': [
                recovered.loc[(recovered['Country/Region'] == country)][date].sum() for date in time_series_date_list
            ],
            'confirmed': [
                confirmed.loc[(confirmed['Country/Region'] == country)][date].sum() for date in time_series_date_list
            ],
            'deaths': [
                deaths.loc[(deaths['Country/Region'] == country)][date].sum() for date in time_series_date_list
            ]
        }, index=time_series_date_list)

    return {
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': '{country} COVID-19 Cases'.format(country=country),
            'barmode': 'stack'
        }

    }

if __name__ == '__main__':
    app.run_server(debug=config['DEBUG'])

