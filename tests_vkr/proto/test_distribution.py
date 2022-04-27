import tempfile

import allure
import plotly.graph_objects as go
import pytest
from plotly.subplots import make_subplots

from VKR_project.tests_vkr.tools.ADV import AvgCampaign


@allure.feature('Distributions')
@allure.story('Test draws a graph with the main indicators of an advertising campaign')
@pytest.mark.parametrize('start_date', ['01.01.2010'])
@pytest.mark.parametrize('end_date', ['10.01.2010'])
@pytest.mark.parametrize('sum_cost', [8000])
def test_create_adv_compaign(start_date, end_date, sum_cost):
    """draw a distribution schedule as part of an advertising campaign"""
    a = AvgCampaign(
        name='Test campain',
        start_date=start_date,
        end_date=end_date,
        sum_cost=sum_cost
    )
    statistic_date = []
    statistic_cost = []
    statistic_clicks = []
    statistic_impressions = []
    statistic_cpc = []
    for i in a.campaign:
        statistic_date.append(i.date)
        statistic_cost.append(i.cost)
        statistic_impressions.append(i.impressions)
        statistic_cpc.append(i.avg_cpc)
        statistic_clicks.append(i.clicks)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=statistic_date, y=statistic_cpc,
                             mode='lines',
                             name='ctr',
                             ), secondary_y=True,)
    fig.add_trace(go.Bar(x=statistic_date, y=statistic_cost, name='cost'))
    fig.add_trace(go.Bar(x=statistic_date, y=statistic_clicks, name='clicks'))
    fig.add_trace(go.Bar(x=statistic_date, y=statistic_impressions, name='impressions'))

    temp = tempfile.NamedTemporaryFile()
    fig.write_html(f'{temp.name}')
    allure.attach.file(f'{temp.name}', attachment_type=allure.attachment_type.HTML)
    assert sum(statistic_cost) == sum_cost
