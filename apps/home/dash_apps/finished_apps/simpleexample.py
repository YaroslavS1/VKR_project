# import dash_core_components as dcc
import dash_html_components as html
# import dash
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)


# app.layout = html.Div([
#     html.H1('Square Root Slider Graph'),
#     dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
#     dcc.Slider(
#         id='slider-updatemode',
#         marks={i: '{}'.format(i) for i in range(20)},
#         max=20,
#         value=2,
#         step=1,
#         updatemode='drag',
#     ),
# ])
#
#
# @app.callback(
#                Output('slider-graph', 'figure'),
#               [Input('slider-updatemode', 'value')])
# def display_value(value):
#
#
#     x = []
#     for i in range(value):
#         x.append(i)
#
#     y = []
#     for i in range(value):
#         y.append(i*i)
#
#     graph = go.Scatter(
#         x=x,
#         y=y,
#         name='Manipulate Graph'
#     )
#     layout = go.Layout(
#         paper_bgcolor='#27293d',
#         plot_bgcolor='rgba(0,0,0,0)',
#         xaxis=dict(range=[min(x), max(x)]),
#         yaxis=dict(range=[min(y), max(y)]),
#         font=dict(color='white'),
#
#     )
#     return {'data': [graph], 'layout': layout}


from dash import dash_table
import pandas as pd
from collections import OrderedDict
import dash_bootstrap_components as dbc

data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(data)
app = DjangoDash('SimpleExample')
app.layout = html.Div(children=[
    html.Div(children=[
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_header={'border': '1px solid black'},
            style_cell={'border': '1px solid grey'},
            style_data={
                # 'backgroundColor': '#F2F4F6',
                'white-space': 'nowrap'},
            # style_as_list_view=True,
            page_size=10,
            page_action='native',
            editable=True,
            # filter_action="native",
            sort_action="native",
            sort_mode='multi',
            style_as_list_view=True,
        ), ]), ],

    style={'display': 'inline-block', 'width': '100%'})
