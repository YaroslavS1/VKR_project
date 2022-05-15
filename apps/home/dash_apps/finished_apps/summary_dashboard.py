import dash_core_components as dcc
import dash_html_components as html
import dash

from ._source.app import app
from ._source.layouts import sales
from ._source import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/sales-overview':
        return sales
    else:
        return sales  # This is the "home page"
