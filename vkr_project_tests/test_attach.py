import logging
import os
import tempfile

import allure
import pandas as pd
import plotly.express as px
import pytest

LOGGER = logging.getLogger(__name__)

@allure.step('test csv')
@pytest.mark.parametrize('file', ['cashe0.csv', 'cashe1.csv', 'cashe2.csv'])
def test_count_summary_cost_ads(file):
    """Calculation of the total cost of advertising"""
    LOGGER.debug(f'{os. getcwd()}')
    f_data = pd.read_csv(f'./case/{file}', header=1, sep='	', index_col=0)
    f_data['Cost'] = pd.to_numeric(f_data["Cost"], downcast='float')
    f_data['Cost'] = f_data['Cost'] / 1000000
    summary_cost = float(f_data.groupby('CampaignName').sum().reset_index()['Cost'])
    f = f_data.groupby('Date').sum().reset_index()
    trace1 = px.line(
        x=f['Date'],
        y=f['Cost'],)
    temp = tempfile.NamedTemporaryFile()
    trace1.write_html(f'{temp.name}')
    allure.attach.file(f'{temp.name}', attachment_type=allure.attachment_type.HTML)

    print((sum(f['Cost'])))
    print(summary_cost)
    assert round(summary_cost, 5) == round(sum(f['Cost']), 5)


@allure.step('API Direct test')
@pytest.mark.parametrize('step', ['1', '2', '3'])
def test_api_direct(step):
    assert step in ['1', '2', '3']
