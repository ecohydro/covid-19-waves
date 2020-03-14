import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app

import plotly.express as px

from functions import get_time_series, get_daily_reports, get_date_list
confirmed, deaths, recovered = get_time_series(local=True)
daily_report_data, dates = get_daily_reports(local=True)

date_list = get_date_list(dates)

def make_country_labels(by_cases=False):
    
    if by_cases == False:
        countries = sorted(confirmed['Country/Region'].drop_duplicates())
    elif by_cases == True:
        countries = list(confirmed.groupby('Country/Region').sum()[date_list[-1]].sort_values(ascending=False).index)

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
    dcc.Graph(id='global-graph')
])

@app.callback(Output('global-graph', 'options'), [Input()])

@app.callback(Output('global-graph', 'figure'), [Input('global-dropdown', 'value')])
def update_global_graph(selected_dropdown_value):
    country = selected_dropdown_value
    if country == None or country == 'Global':
        df = pd.DataFrame(
            data={
                'confirmed': [confirmed[date].sum() for date in date_list],
                'deaths': [deaths[date].sum() for date in date_list],
                'recovered': [recovered[date].sum() for date in date_list]
            }, index=date_list)
    else:
        df = pd.DataFrame(
        data={
            'recovered': [
                recovered.loc[(recovered['Country/Region'] == country)][date].sum() for date in date_list
            ],
            'confirmed': [
                confirmed.loc[(confirmed['Country/Region'] == country)][date].sum() for date in date_list
            ],
            'deaths': [
                deaths.loc[(deaths['Country/Region'] == country)][date].sum() for date in date_list
            ]
        }, index=date_list)

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
    app.run_server(debug=True)
