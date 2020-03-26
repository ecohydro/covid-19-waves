# -*- coding: utf-8 -*-
import dash
import plotly as py
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from config import config

from layouts import global_tab, US_tab, pandemic_tab

from data import (
    confirmed, deaths, #recovered,
    time_series_dates, daily_report_data, daily_dates, time_series_date_list,
    daily_date_list, #  us_recovered,
    us_deaths, us_confirmed,
    dates, date_strings, label_dict, data_df, data_by_area,
    make_data_global, make_data_state
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
            dcc.Tab(
                label='Analysis',
                value='tab-3-main',
                className='custom-tab',
                selected_className='custom-tab--selected')
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
    if tab == 'tab-3-main':
        return pandemic_tab

# Gather functions for making graphs:
from model import (
    last_update, ndays
    )


@app.callback(Output('updatemode-output-container', 'children'),
              [Input('crossfilter-date--slider', 'value')])
def display_value(value):
    return 'Date: {} '.format(date_strings[value])

@app.callback(
    dash.dependencies.Output(
        component_id='crossfilter-xaxis-column',
        component_property='options'),
    [dash.dependencies.Input('charlie-sort','value')])
def update_xaxis_dropdown(sort):
    from data import variable_dict
    if sort == 'Charlie Sort':
        return [{'label':label, 'value':variable,} for label, variable in sorted(variable_dict.items())]
    else:
        return [{'label':label, 'value':variable,} for label, variable in variable_dict.items()]

@app.callback(
    dash.dependencies.Output(
        component_id='crossfilter-yaxis-column',
        component_property='options'),
    [dash.dependencies.Input('charlie-sort','value')])
def update_yaxis_dropdown(sort):
    from data import variable_dict
    if sort == 'Charlie Sort':
        return [{'label':label, 'value':variable,} for label, variable in sorted(variable_dict.items())]
    else:
        return [{'label':label, 'value':variable,} for label, variable in variable_dict.items()]


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     #dash.dependencies.Input('crossfilter-threshold--slider', 'value'),
     dash.dependencies.Input('crossfilter-date--slider', 'value')])
def update_scatter_graph(
    xaxis_column_name,
    yaxis_column_name,
    xaxis_type, yaxis_type,
    #threshold_value,
    date_value):
    date = date_strings[date_value]
    dff = data_df[data_df['date'] == date]
    return {
        'data': [dict(
            x=dff[dff['variable'] == xaxis_column_name]['value'],
            y=dff[dff['variable'] == yaxis_column_name]['value'],
            text=dff[dff['variable'] == yaxis_column_name]['country'],
            customdata=dff[dff['variable'] == yaxis_column_name]['country'],
            mode='markers',
            marker={
                'size':15,
                'opacity':0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': label_dict[xaxis_column_name],
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': label_dict[yaxis_column_name],
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 80, 'r': 40},
            height=500,
            hovermode='closest',
            title='Global Data, {date}'.format(date=date_strings[date_value])
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [dict(
            x=dff['date'],
            y=dff['value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 40, 'b': 100, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = data_df[data_df['country'] == country_name]
    dff = dff[dff['variable'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, label_dict[xaxis_column_name])
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = data_df[data_df['country'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['variable'] == yaxis_column_name]
    return create_time_series(dff, axis_type, label_dict[yaxis_column_name])


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
            # {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
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
            # {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
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
            # {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
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
            # {'y': df['recovered'], 'x': df.index, 'type': 'bar', 'name': 'Recovered'},
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

