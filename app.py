# -*- coding: utf-8 -*-
import dash
import plotly as py
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
    dcc.Tabs(
        id="tabs-main", value='tab-1-main', 
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Global',
                value='tab-1-main',
                className='custom-tab',
                selected_className='custom-tab--selected'),
            dcc.Tab(
                label='United States',
                value='tab-2-main',
                className='custom-tab',
                selected_className='custom-tab--selected'
                ),
    ]),
    html.Div(id='tabs-content-main'),
    html.Div(children=[
        html.A('Code on Github', href=githublink),
        html.Br(),
        html.A('Data Source', href=sourceurl)
        ],style={'width':'80%','margin':'0 auto'})
])

@app.callback(Output('tabs-content-main', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-1-main':
        return global_tab
    if tab == 'tab-2-main':
        return US_tab


# Gather functions for making graphs:
from model import data_by_area, last_update, make_data_global, make_data_state


# @app.callback(Output('combo-graph', 'figure'), [Input('global-dropdown', 'value')])
# def update_combo_global_graph(country):
#     template='<br>%{x}:%{y}<br>'
#     df = make_data_global(country)
#     df_diff = df.diff()
#     fig = py.subplots.make_subplots(
#         rows=2, cols=1,
#         shared_xaxes=True,
#         vertical_spacing=0.1,
#         #horizontal_spacing=0.009,
#         subplot_titles=['Total Cases', 'Daily Cases']
#     )
#     # fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 10, 't': 10}
#     #fig['layout']['barmode'] = 'stack'
#     fig.append_trace(
#         {'x':df.index,'y':df['confirmed'],
#         'type':'scatter',
#         'hovertemplate':template,
#         'name':'Total Confirmed'},1,1)
#     fig.append_trace(
#         {'x':df.index,'y':df['recovered'],
#         'type':'scatter',
#         'hovertemplate':template,
#         'name':'Total Recovered'},1,1)
#     fig.append_trace(
#         {'x':df.index,'y':df['deaths'],
#         'type':'scatter',
#         'hovertemplate':template,
#         'name':'Total Deaths'},1,1)
#     fig.append_trace(
#         {'x':df.index,'y':df_diff['confirmed'],
#         'type':'bar',
#         'hovertemplate':template,
#         'name':'Daily Confirmed'},2,1)
#     fig.append_trace(
#         {'x':df.index,'y':df_diff['recovered'],
#         'type':'bar',
#         'hovertemplate':template,
#         'name':'Daily Recovered'},2,1)
#     fig.append_trace(
#         {'x':df.index,'y':df_diff['deaths'],
#         'type':'bar',
#         'hovertemplate':template,
#         'name':'Daily Deaths'},2,1)
#     fig.update_layout(
#         autosize=True,
#         #width=700,
#         height=700,
#         margin=dict(
#             l=50,
#             r=50,
#             b=100,
#             t=50,
#             pad=4
#         ),
#         paper_bgcolor="white",
#     )
#     return fig

@app.callback(Output('global-daily-graph', 'figure'), [Input('global-dropdown', 'value')])
def update_global_daily_graph(selected_dropdown_value):
     country = selected_dropdown_value
     df = make_data_global(country)
     df = df.diff()
     return {
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': 'Daily {country} COVID-19 Cases, Last Updated {update}'.format(
                country=country,
                update=last_update(country).strftime("%B %d, %Y")),
            #'margin':{'l': 40, 'b': 40, 't': 10, 'r': 10}
        }
    }

@app.callback(Output('global-graph', 'figure'), [Input('global-dropdown', 'value')])
def update_global_graph(selected_dropdown_value):
    country = selected_dropdown_value
    df = make_data_global(country)
    return {
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': '{country} COVID-19 Cases, Last Updated {update}'.format(
                country=country,
                update=last_update(country).strftime("%B %d, %Y")),
            'barmode': 'stack',
            #'margin':{'l': 40, 'b': 40, 't': 10, 'r': 10}
        }
    }

@app.callback(Output('us-daily-graph', 'figure'), [Input('us-dropdown', 'value')])
def update_us_daily_graph(state):
     df = make_data_state(state)
     df = df.diff()
     return {
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': 'Daily {state} COVID-19 Cases'.format(
                state=state),
            'height':350,
            'margin':dict(
            l=50,
            r=50,
            b=100,
            t=50,
            pad=4
            ),
            'paper_bgcolor':"white",
        }
    }

@app.callback(Output('us-graph', 'figure'), [Input('us-dropdown', 'value')])
def update_us_graph(state):
    df = make_data_state(state)
    return {    
        'data': [
            {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
            {'y': df['confirmed'], 'x': df.index, 'type': 'bar', 'name': 'Confirmed'},
            {'y': df['deaths'], 'x': df.index, 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': '{state} COVID-19 Cases, Last Updated {update}'.format(
                state=state,
                update=last_update(state, column='State').strftime("%B %d, %Y")),
            'barmode': 'stack',
            'height':350,
            'margin':dict(
            l=50,
            r=50,
            b=100,
            t=50,
            pad=4
            ),
            'paper_bgcolor':"white",
        }
    }
#confirmed[(confirmed['Country/Region'] == 'US') & (confirmed['Province/State'] == 'Nebraska')]

if __name__ == '__main__':
    app.run_server(debug=config['DEBUG'])

