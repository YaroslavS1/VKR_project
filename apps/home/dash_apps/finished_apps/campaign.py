from collections import OrderedDict

import pandas as pd
from apps.home.views import adv, crm
from dash import dash_table, html
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

labels = [(i['source'].unique()[0], i['name'].unique()[0]) for i in adv]
costs = [i['cost'].sum() for i in adv]
profits = [crm.loc[crm['name'] == i[1]]['profit'].sum() for i in labels]
visits = [i['clicks'].sum() for i in adv]
impressions = [i['impressions'].sum() for i in adv]
payments = [crm.loc[crm['name'] == i[1]]['payment'].sum() for i in labels]


data = OrderedDict(
    [
        ("Источник", [i[0] for i in labels]),
        ("Рекламная кампания", [i[1] for i in labels]),
        ("Стоимость", costs),
        ("Показы", impressions),
        ("Визиты", visits),
        ('ROI', [round((profit - cost) / cost * 100, 2) for cost, profit in zip(costs, profits)]),
        ('Число покупок', payments),
        ("Конверсия", [round((payment / vizit) * 100, 2) for payment, vizit in zip(payments, visits)]),
        ("AVG CPC", [round((cost / vizit), 2) for cost, vizit in zip(costs, visits)]),
        ("AOV", [round((profit / payment), 2) for profit, payment in zip(profits, payments)]),
        ("CPО", [round((costs / payment), 2) for costs, payment in zip(costs, payments)]),
        ("CTR", [round((vizit / impression) * 100, 2) for impression, vizit in zip(impressions, visits)]),
        ("Приыбль", [round(i, 2) for i in profits])
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
                    'filter_query': '{ROI} > 0',
                    'column_id': 'ROI'
                },
                'color': 'green',
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'filter_query': '{ROI} = 0',
                    'column_id': 'ROI'
                },
                'color': 'blue',
                'fontWeight': 'bold'
            },
        ],
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True
    ),
    html.Div(id='datatable-interactivity-container')
])
