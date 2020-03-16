import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from data import country_labels, state_labels

global_tab = html.Div(children=[
    html.H3(children=[
        'Select a Country'],style={'width':'30%','margin':'0 auto'}),
    html.Div(children=[
            dcc.Dropdown(
                id='global-dropdown',
                options=country_labels,
                value='Global'
            )],style={'width':'30%', 'margin':'0 auto'}),
    # html.Div(children=[dcc.Graph(id='global-graph')]),
    # html.Div(children=[dcc.Graph(id='global-daily-graph')])
    html.Div(
    	children=[dcc.Graph(id='combo-graph')],
    	style={'width':'80%','margin':'0 auto'}
    )
    ])
	


US_tab = html.Div(children=[
	html.H3(children=[
        'Select a State'],style={'width':'30%','margin':'0 auto'}),
    html.Div(children=[
            dcc.Dropdown(
                id='us-dropdown',
                options=state_labels,
                value='National'
            )],style={'width':'30%', 'margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='us-graph')],style={'width':'80%','margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='us-daily-graph')],style={'width':'80%','margin':'0 auto'})
])
