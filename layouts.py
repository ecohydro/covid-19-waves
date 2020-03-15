import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from data import country_labels, state_labels

global_tab = html.Div(children=[
    html.Div(children=[
        'Select a Country'],style={'width':'80%','align':'right'}),
    html.Div(children=[
            dcc.Dropdown(
                id='global-dropdown',
                options=country_labels,
                value='Global'
            )],style={'width':'20%'}),
    dcc.Graph(id='global-graph'),
    dcc.Graph(id='global-model-graph')
    ])
	


US_tab = html.Div(children=[
	html.Div(children=[
        'Select a State'],style={'width':'80%','align':'right'}),
    html.Div(children=[
            dcc.Dropdown(
                id='us-dropdown',
                options=state_labels,
                value='National'
            )],style={'width':'20%'}),
    dcc.Graph(id='us-graph')])
