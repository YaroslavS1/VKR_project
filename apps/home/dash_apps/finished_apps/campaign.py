from collections import OrderedDict

import pandas as pd
from apps.home.views import _a1, _a2, _crm
from dash import dash_table, html
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
a1 = _a1.info_
a2 = _a2.info_
crm = _crm.adv
# print(round(crm[a1[-2], a1[-1]][-1] / crm[a1[-2], a1[-1]][-2], 2), round(crm[a2[-2], a2[-1]][-1] / crm[a2[-2], a2[-1]][-2], 2))
data = OrderedDict(
    [
        ("Источник", [a1[-2], a2[-2]]),
        ("Рекламная кампания", [a1[-1], a2[-1]]),
        ("ROI", [round((crm[a1[-2], a1[-1]][-1] - a1[3]) / a1[3] * 100, 2),
                 round((crm[a2[-2], a2[-1]][-1] - a2[3]) / a2[3] * 100, 2)]),
        ("Визиты", [round(crm[a1[-2], a1[-1]][0], 2), round(crm[a2[-2], a2[-1]][0], 2)]),
        ("Конверсия", [round(crm[a1[-2], a1[-1]][0] / crm[a1[-2], a1[-1]][2], 2),
                       round(crm[a2[-2], a2[-1]][2] / crm[a2[-2], a2[-1]][2], 2)]),
        ("CPC", [round(a1[3] / a1[1], 2), round(a2[3] / a2[1], 2)]),
        ("AOV", [round(crm[a1[-2], a1[-1]][-1] / crm[a1[-2], a1[-1]][-2], 2),
                 round(crm[a2[-2], a2[-1]][-1] / crm[a2[-2], a2[-1]][-2], 2)])
        # ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        # ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        # ("Humidity", [10, 20, 30, 40, 50, 60]),
        # ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)
# advertising_summary_table
df = pd.DataFrame(data)
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
app = DjangoDash('CampaignTable', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        # page_current= 0,
        # page_size= 10,
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{ROI} < 0',
                    'column_id': 'ROI'
                },
                'color': 'red',
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'filter_query': '{ROI} > 1',
                    'column_id': 'ROI'
                },
                'color': 'green',
                'fontWeight': 'bold'
            },
        ],
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True
    ),
    html.Div(id='datatable-interactivity-container')
])
