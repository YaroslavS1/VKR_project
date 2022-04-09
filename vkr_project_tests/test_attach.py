import tempfile

import allure
import pandas as pd
import plotly.express as px
import pytest


@pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
def test_count_summary_cost_ads():
    """Calculation of the total cost of advertising"""
    '''
    суть теста разложить сколько мы заплатили по дням 
    распечатать это 
    и ссумировать 
    '''
    f_data = pd.read_csv("../case/cashe.csv", header=1, sep='	', index_col=0, )
    f_data['Cost'] = pd.to_numeric(f_data["Cost"], downcast='float')
    f_data['Cost'] = f_data['Cost'] / 1000000
    summary_cost = float(f_data.groupby('CampaignName').sum().reset_index()['Cost'])
    f = f_data.groupby('Date').sum().reset_index()
    trace1 = px.line(
        x=f['Date'],
        y=f['Cost'],)
    # fig.add_trace(trace1, row=1, col=1)
    # # fig.add_trace(trace2, row=2, col=1)
    # # fig.add_trace(trace3, row=3, col=1)
    #
    # fig.update_layout(xaxis=dict(tickangle=90))
    temp = tempfile.NamedTemporaryFile()
    print(temp.name)
    # fp.write()
    trace1.write_html(f'{temp.name}')
    allure.attach.file('temp.name', attachment_type=allure.attachment_type.HTML)
    print((sum(f['Cost'])))
    print(summary_cost)
    # assert False


@pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
def test_xfail_unexpected_pass():
    """this test is an xfail that will be marked as unexpected success"""
    assert True

@pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
def test_xfail_unexpected_pass__():
    """this test is an xfail that will be marked as unexpected success"""
    assert True


@pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
def test_xfail_unexpected_pass___():
    """this test is an xfail that will be marked as unexpected success"""
    assert False

