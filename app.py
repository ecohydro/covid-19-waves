# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from functions import get_time_series, get_daily_reports

time_series_data = get_time_series()
daily_report_data = get_daily_reports()

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


# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])

# app.layout = html.Div(style={'backgroundColor': colors['background']},
# 	children=[
#     	html.H1(
#     		children='COVID-19 Data Dashboard',
#     		style={
#          	   'textAlign': 'center',
#             	'color': colors['text']
#         	}
#     	),

# 	    html.Div(
# 	    	children='Graphing & plotting tools for visualizing COVID-19 data aggregated by the <a href=https://github.com/CSSEGISandData/COVID-19>CSSE</a> at Johns Hopkins University.',
# 	    	style={
# 	    		'textAlign': 'center',
#         		'color': colors['text']
#         	}
#         ),
# 	    html.Div(id='graph-input'),
# 	    html.H1(id='graph-output')

# ])

# @app.callback(Output(component_id='graph-output', component_property='children'),
# 			  [Input(component_id='graph-input', component_property='')])
# def make_global_graph(df):
# 	return dcc.Graph(
#         	id='example-graph',
#         	figure={
#          	   'data': [
#           	      {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#           	      {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#           	  	],
#             	'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
#                 	}
#         		}
#     		}
#     	)



# if __name__ == '__main__':
#     app.run_server(debug=True)
