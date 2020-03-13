import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app
from layouts import layout_global, layout_us, layout_ca, layout_index
import callbacks

from data import totals_by_day

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>COVID-19 Dashboard</title>
#         {%favicon%}
#         {%css%}
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#         </footer>
#         <div>WAVES Lab, Earth Research Institute</div>
#     </body>
# </html>
# '''

app.layout = html.Div([
    html.H1(children='COVID-19 Dashboard'),

    html.Div(children='''
        Data from Johns Hopkins.
    '''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'y': totals_by_day['confirmed'], 'x': totals_by_day.index, 'type': 'bar', 'name': 'Confirmed'},
                {'y': totals_by_day['deaths'], 'x': totals_by_day.index, 'type': 'bar', 'name': 'Deaths'},
                {'y': totals_by_day['recovered'], 'x': totals_by_day.index, 'type': 'bar', 'name': 'Recovered'}
            ],
            'layout': {
                'title': 'Global COVID-19 Cases'
            }
        }
    )
])

# Update page
# # # # # # # # #
# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/global':
#         return layout_global
#     elif pathname == '/us':
#         return layout_us
#     elif pathname == '/california':
#         return layout_ca
#     elif pathname == '/':
#     	return layout_index
#     else:
#         return noPage

# # # # # # # # #
# external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
#                 "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
#                 "//fonts.googleapis.com/css?family=Raleway:400,300,600",
#                 "https://codepen.io/bcd/pen/KQrXdb.css",
#                 "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
#                 "https://codepen.io/dmcomfort/pen/JzdzEZ.css"]

# for css in external_css:
#     app.css.append_css({"external_url": css})

# external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#                "https://codepen.io/bcd/pen/YaXojL.js"]

# for js in external_js:
#     app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=True)
