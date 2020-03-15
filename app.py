# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from config import config

from layouts import global_tab, US_tab

from data import (
    confirmed, deaths, recovered, time_series_dates,
    daily_report_data, daily_dates, time_series_date_list,
    daily_date_list, us_recovered, us_deaths, us_confirmed,
#    county_recovered, county_deaths, county_confirmed,
#    state_confirmed, state_recovered, state_deaths
    )


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
    external_stylesheets=external_stylesheets)

app.title = 'WAVES Lab COVID-19 Dashboard'
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1(children='COVID-19 Dashboard'),
    dcc.Tabs(id="tabs-main", value='tab-1-main', children=[
        dcc.Tab(label='Global', value='tab-1-main'),
        dcc.Tab(label='United States', value='tab-2-main'),
    ]),
    html.Div(id='tabs-content-main'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
])

@app.callback(Output('tabs-content-main', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-1-main':
        return global_tab
    if tab == 'tab-2-main':
        return US_tab


# Gather functions for making graphs:
from model import data_by_area, last_update

# @app.callback(Output('global-model-graph', 'figure'), [Input('global-dropdown', 'value')])
# def update_global_model_graph(selected_dropdown_value):
#     country = selected_dropdown_value
#     if country == None or country == 'Global':
#         df = pd.DataFrame(
#             )

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
            # These dictionaries need to include lists, not pd.Series!
            'recovered': data_by_area(area=country, df=recovered).tolist(),
            'confirmed': data_by_area(area=country, df=confirmed).tolist(),
            'deaths': data_by_area(area=country, df=deaths).tolist()
        }, index=time_series_date_list)

    return {
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': '{country} COVID-19 Cases, Last Updated {update}'.format(
                country=country,
                update=last_update(country)),
            'barmode': 'stack'
        }
    }

@app.callback(Output('us-graph', 'figure'), [Input('us-dropdown', 'value')])
def update_us_graph(selected_dropdown_value):
    from functions import us_state_abbrev
    state = selected_dropdown_value
    if state == None or state == 'National':
        df = pd.DataFrame(
            data={
                'confirmed': [us_confirmed[date].sum() for date in time_series_date_list],
                'deaths': [us_deaths[date].sum() for date in time_series_date_list],
                'recovered': [us_recovered[date].sum() for date in time_series_date_list]
            }, index=time_series_date_list)
    else:
        df = pd.DataFrame(
            data={
            'recovered': data_by_area(area=state, df=us_recovered, col='State').tolist(),
            'confirmed': data_by_area(area=state, df=us_confirmed, col='State').tolist(),
            'deaths': data_by_area(area=state, df=us_deaths, col='State').tolist()
        }, index=time_series_date_list)

    return {
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': '{state} COVID-19 Cases'.format(state=state),
            'barmode': 'stack'
        }
    }
#confirmed[(confirmed['Country/Region'] == 'US') & (confirmed['Province/State'] == 'Nebraska')]

if __name__ == '__main__':
    app.run_server(debug=config['DEBUG'])

