import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from functions import make_country_labels, make_state_labels

global_tab = html.Div(children=[
    html.Div(children=[
        'Select a Country'],style={'width':'80%','align':'right'}),
    html.Div(children=[
            dcc.Dropdown(
                id='global-dropdown',
                options=make_country_labels(by_cases=True),
                value='Global'
            )],style={'width':'20%'}),
    dcc.Graph(id='global-graph')])


US_tab = html.Div(children=[
	html.Div(children=[
        'Select a State'],style={'width':'80%','align':'right'}),
    html.Div(children=[
            dcc.Dropdown(
                id='us-dropdown',
                options=make_state_labels(by_cases=True),
                value='National'
            )],style={'width':'20%'}),
    dcc.Graph(id='us-graph')])
